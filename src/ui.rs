use std::io;
use std::time::Duration;
use std::sync::Arc;

use ratatui::{
    backend::{Backend, CrosstermBackend},
    layout::{Constraint, Direction, Layout, Rect},
    style::{Color, Modifier, Style},
    text::{Line, Span},
    widgets::{Block, Borders, List, ListItem, Paragraph, Chart, Dataset, Axis, GraphType},
    Frame, Terminal,
};
use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};

use crate::{Metric, ClogTracker};

pub struct TerminalUI {
    pub search_query: String,
    pub selected_metric: Option<String>,
    pub input_mode: InputMode,
    tracker: Arc<ClogTracker>,
}

#[derive(Debug, PartialEq)]
pub enum InputMode {
    Normal,
    Searching,
}

impl TerminalUI {
    pub fn new(tracker: Arc<ClogTracker>) -> Self {
        TerminalUI {
            search_query: String::new(),
            selected_metric: None,
            input_mode: InputMode::Normal,
            tracker,
        }
    }

    pub fn run(&mut self) -> Result<(), io::Error> {
        enable_raw_mode()?;
        let mut stdout = io::stdout();
        execute!(stdout, EnterAlternateScreen, EnableMouseCapture)?;
        let backend = CrosstermBackend::new(stdout);
        let mut terminal = Terminal::new(backend)?;

        let res = self.run_app(&mut terminal);

        disable_raw_mode()?;
        execute!(
            terminal.backend_mut(),
            LeaveAlternateScreen,
            DisableMouseCapture
        )?;
        terminal.show_cursor()?;

        if let Err(err) = res {
            println!("{:?}", err);
        }
        Ok(())
    }

    fn run_app<B: Backend>(&mut self, terminal: &mut Terminal<B>) -> io::Result<()> {
        loop {
            terminal.draw(|f| self.ui(f))?;

            if event::poll(Duration::from_millis(100))? {
                if let Event::Key(key) = event::read()? {
                    match self.input_mode {
                        InputMode::Normal => match key.code {
                            KeyCode::Char('q') | KeyCode::Esc => return Ok(()),
                            KeyCode::Char('/') => {
                                self.input_mode = InputMode::Searching;
                            }
                            KeyCode::Down => self.next_metric(),
                            KeyCode::Up => self.previous_metric(),
                            _ => {}
                        },
                        InputMode::Searching => match key.code {
                            KeyCode::Char(c) => {
                                self.search_query.push(c);
                            }
                            KeyCode::Backspace => {
                                self.search_query.pop();
                            }
                            KeyCode::Enter | KeyCode::Esc => {
                                self.input_mode = InputMode::Normal;
                            }
                            _ => {}
                        },
                    }
                }
            }
        }
    }

    fn ui(&self, f: &mut Frame) {
        let chunks = Layout::default()
            .direction(Direction::Vertical)
            .constraints([
                Constraint::Length(3),
                Constraint::Min(10),
                Constraint::Length(10),
            ])
            .split(f.area());

        // Search bar
        let search_widget = Paragraph::new(self.search_query.as_str())
            .style(match self.input_mode {
                InputMode::Normal => Style::default(),
                InputMode::Searching => Style::default().fg(Color::Yellow),
            })
            .block(Block::default().borders(Borders::ALL).title("Search"));
        f.render_widget(search_widget, chunks[0]);

        // Metrics area
        let metrics_chunks = Layout::default()
            .direction(Direction::Horizontal)
            .constraints([Constraint::Percentage(30), Constraint::Percentage(70)])
            .split(chunks[1]);

        // Metrics list
        self.render_metrics_list(f, metrics_chunks[0]);

        // Selected metric chart
        self.render_metric_chart(f, metrics_chunks[1]);

        // Logs area
        self.render_logs(f, chunks[2]);
    }

    fn render_metrics_list(&self, f: &mut Frame, area: Rect) {
        let metrics = self.tracker.metrics.lock().unwrap();
        let filtered_metrics: Vec<(&String, &Vec<Metric>)> = metrics
            .iter()
            .filter(|(name, _)| {
                self.search_query.is_empty() || name.contains(&self.search_query)
            })
            .collect();

        let items: Vec<ListItem> = filtered_metrics
            .iter()
            .map(|(name, values)| {
                let style = if Some((*name).clone()) == self.selected_metric {
                    Style::default().fg(Color::Yellow).add_modifier(Modifier::BOLD)
                } else {
                    Style::default()
                };
                let last_value = values.last().map_or(0.0, |m| m.value);
                ListItem::new(Line::from(Span::raw(format!("{}: {:.3}", name, last_value))))
                    .style(style)
            })
            .collect();

        let list = List::new(items)
            .block(Block::default().borders(Borders::ALL).title("Metrics"));
        
        f.render_widget(list, area);
    }

    fn render_metric_chart(&self, f: &mut Frame, area: Rect) {
        if let Some(selected) = &self.selected_metric {
            let metrics = self.tracker.metrics.lock().unwrap();
            if let Some(data) = metrics.get(selected) {
                let points: Vec<(f64, f64)> = data
                    .iter()
                    .map(|m| (m.step as f64, m.value))
                    .collect();

                let datasets = vec![Dataset::default()
                    .name(selected.as_str())
                    .marker(ratatui::symbols::Marker::Dot)
                    .graph_type(GraphType::Line)
                    .style(Style::default().fg(Color::Cyan))
                    .data(&points)];

                let x_bounds = [
                    points.first().map_or(0.0, |p| p.0),
                    points.last().map_or(1.0, |p| p.0),
                ];
                let y_bounds = [
                    points.iter().map(|p| p.1).fold(f64::INFINITY, f64::min),
                    points.iter().map(|p| p.1).fold(f64::NEG_INFINITY, f64::max),
                ];

                let chart = Chart::new(datasets)
                    .block(Block::default().borders(Borders::ALL).title(selected.as_str()))
                    .x_axis(Axis::default().bounds(x_bounds).labels(vec![
                        Span::raw(format!("{}", x_bounds[0])),
                        Span::raw(format!("{}", x_bounds[1])),
                    ]))
                    .y_axis(Axis::default().bounds(y_bounds).labels(vec![
                        Span::raw(format!("{:.2}", y_bounds[0])),
                        Span::raw(format!("{:.2}", y_bounds[1])),
                    ]));

                f.render_widget(chart, area);
            }
        } else {
            let placeholder = Paragraph::new("Select a metric to view")
                .block(Block::default().borders(Borders::ALL).title("Chart"));
            f.render_widget(placeholder, area);
        }
    }

    fn render_logs(&self, f: &mut Frame, area: Rect) {
        let logs = self.tracker.logs.lock().unwrap();
        let items: Vec<ListItem> = logs
            .iter()
            .rev()
            .take(area.height as usize - 2)
            .map(|log| {
                let style = match log.level {
                    crate::LogLevel::Info => Style::default(),
                    crate::LogLevel::Warning => Style::default().fg(Color::Yellow),
                    crate::LogLevel::Error => Style::default().fg(Color::Red),
                };
                ListItem::new(Line::from(Span::raw(format!(
                    "[{}] {}",
                    log.timestamp.format("%H:%M:%S"),
                    log.message
                ))))
                .style(style)
            })
            .collect();

        let list = List::new(items)
            .block(Block::default().borders(Borders::ALL).title("Logs"));
        
        f.render_widget(list, area);
    }

    fn next_metric(&mut self) {
        let metrics = self.tracker.metrics.lock().unwrap();
        let names: Vec<String> = metrics
            .keys()
            .filter(|name| self.search_query.is_empty() || name.contains(&self.search_query))
            .cloned()
            .collect();

        if names.is_empty() {
            return;
        }

        match &self.selected_metric {
            None => self.selected_metric = Some(names[0].clone()),
            Some(current) => {
                if let Some(pos) = names.iter().position(|n| n == current) {
                    self.selected_metric = Some(names[(pos + 1) % names.len()].clone());
                } else {
                    self.selected_metric = Some(names[0].clone());
                }
            }
        }
    }

    fn previous_metric(&mut self) {
        let metrics = self.tracker.metrics.lock().unwrap();
        let names: Vec<String> = metrics
            .keys()
            .filter(|name| self.search_query.is_empty() || name.contains(&self.search_query))
            .cloned()
            .collect();

        if names.is_empty() {
            return;
        }

        match &self.selected_metric {
            None => self.selected_metric = Some(names.last().unwrap().clone()),
            Some(current) => {
                if let Some(pos) = names.iter().position(|n| n == current) {
                    self.selected_metric = Some(names[if pos == 0 { names.len() - 1 } else { pos - 1 }].clone());
                } else {
                    self.selected_metric = Some(names[0].clone());
                }
            }
        }
    }
}