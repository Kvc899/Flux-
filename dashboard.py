#Source Code Below ⬇️ 
import rumps
import psutil
from AppKit import NSAttributedString, NSForegroundColorAttributeName, NSColor

class Flux(rumps.App):
    def __init__(self):
        super(Flux, self).__init__("⚡️")
        
        self.notify_critical = True 
        self.history_log = []

        # Construct the menu first
        self.setup_menu()
        
        # 3-second update interval
        self.timer = rumps.Timer(self.update_display, 3)
        self.timer.start()

    def setup_menu(self):
        # We create these as sub-menus so they are ready when the app starts
        self.stats_menu = rumps.MenuItem("Top Apps (Live)")
        self.history_menu = rumps.MenuItem("Alert History")
        self.history_menu.add("No recent alerts")

        settings = rumps.MenuItem("Settings")
        self.crit_toggle = rumps.MenuItem("Alert on Red (90%+)", callback=self.toggle_notif)
        self.crit_toggle.state = True
        settings.add(self.crit_toggle)

        self.menu = [self.stats_menu, self.history_menu, None, settings]

    def toggle_notif(self, sender):
        sender.state = not sender.state
        self.notify_critical = sender.state

    def update_stats_menu(self):
        """Safely updates the process list, avoiding 'NoneType' crashes"""
        # SAFETY GUARD 1: Check if the menu actually exists yet
        if not hasattr(self.stats_menu, '_menu') or self.stats_menu._menu is None:
            return

        apps = []
        for proc in psutil.process_iter(['name', 'cpu_percent']):
            try:
                info = proc.info
                # SAFETY GUARD 2: Ignore processes that give 'None' for CPU
                if info['cpu_percent'] is not None:
                    apps.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Sort safely now that we know there are no None types
        top_apps = sorted(apps, key=lambda x: x['cpu_percent'], reverse=True)[:5]
        
        self.stats_menu.clear()
        for app in top_apps:
            self.stats_menu.add(f"{app['name'][:15]}: {int(app['cpu_percent'])}%")

    def set_colored_title(self, text, color):
        """Force the title to update with color and the lightning bolt"""
        full_text = f"⚡️ {text}"
        attributes = {NSForegroundColorAttributeName: color}
        colored_text = NSAttributedString.alloc().initWithString_attributes_(full_text, attributes)
        self._nsapp.nsstatusitem.setAttributedTitle_(colored_text)

    def update_display(self, _):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            bat = psutil.sensors_battery()
            disk = psutil.disk_usage('/').percent
            
            # Update the submenu
            self.update_stats_menu()

            # Build display string
            b_val = bat.percent if bat else "!"
            title_text = f"C:{int(cpu)}% | R:{int(ram)}% | B:{int(b_val)}% | D:{int(disk)}%"
            
            # Update colors based on usage
            if cpu >= 90 or ram >= 90:
                self.set_colored_title(title_text, NSColor.redColor())
                if self.notify_critical:
                    rumps.notification("Flux: Red Alert", "High Usage", f"C:{cpu}% R:{ram}%")
            elif 80 <= cpu <= 89 or 80 <= ram <= 89:
                self.set_colored_title(title_text, NSColor.yellowColor())
            else:
                self.title = f"⚡️ {title_text}"
        except Exception as e:
            # This catch-all prevents the whole app from vanishing if one error occurs
            print(f"Flux logic error: {e}")

if __name__ == "__main__":
    Flux().run()
    #❤️hi👋 
