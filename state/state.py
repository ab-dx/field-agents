import threading
import re
from collections import deque, defaultdict
from datetime import datetime
import json

class AppState:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_state()
        return cls._instance
    
    def _init_state(self):
        """Thread-safe state initialization."""
        self.events = deque(maxlen=200)  # Recent events
        self.kpis = defaultdict(float)   # Metric counters
        self.reports = []                # Review reports
        self.target = ""
        self.reviews_count = 0
        self.lock = threading.RLock()    # For mutations
    
    def add_event(self, event: str):
        """Add cleaned event."""
        with self.lock:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.events.append(f"{event}")
    
    def update_kpi(self, name: str, value: float):
        """Increment KPI."""
        with self.lock:
            self.kpis[name] += value

    def set_target(self, company: str):
        """Set company to research"""
        with self.lock:
            self.target = company

    def get_target(self):
        """Get company to research"""
        return self.target
    
    def add_report(self, report):
        """Store review report."""
        with self.lock:
            self.reports.append({"timestamp": datetime.now().isoformat(), "report": report})
            self.reviews_count += 1
            self.update_kpi("reviews_analyzed", 1)
    
    def get_events_md(self) -> str:
        """Get formatted events for UI."""
        prefixes = [
            r"^(assistant:\s*)?", r"^(user:\s*)?", 
        ]
        response = (self.events[-1]) if len(self.events)>0 else "Thinking..."
        cleaned = response.strip()
        for prefix in prefixes:
            cleaned = re.sub(prefix, "", cleaned, flags=re.IGNORECASE | re.MULTILINE)
        return cleaned if len(cleaned.strip()) > 0 else "Thinking..."
    
    def get_kpis_md(self) -> str:
        """Get KPI dashboard."""
        md = "**📊 KPIs:**\n\n"
        for name, value in sorted(self.kpis.items()):
            md += f"**{name.replace('_', ' ').title()}:** {value:.0f}\n\n"
        md += f"**Total Reports:** {len(self.reports)}\n\n"
        return md
    
    @classmethod
    def instance(cls):
        return cls()

