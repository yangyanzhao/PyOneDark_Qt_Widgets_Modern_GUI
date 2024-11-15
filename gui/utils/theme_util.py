from dayu_widgets import MTheme

from gui.core.json_settings import Settings
from gui.core.json_themes import Themes


def setup_main_theme(widget):
    themes = Themes()
    widget.themes = themes.items
    settings = Settings()
    widget.settings = settings.items
    MTheme(theme="dark").apply(widget)
    m_theme = MTheme()
    m_theme.set_theme(theme="light" if widget.themes['theme_name'] == "bright" else "dark")
    # 自定义主题
    m_theme.title_color = widget.themes["app_color"]["text_title"]
    m_theme.primary_text_color = widget.themes["app_color"]["text_foreground"]
    m_theme.secondary_text_color = widget.themes["app_color"]["text_description"]

    m_theme.background_color = widget.themes["app_color"]["bg_three"]
    m_theme.background_selected_color = "#292929"
    m_theme.background_in_color = widget.themes["app_color"]["bg_two"]
    m_theme.background_out_color = widget.themes["app_color"]["bg_one"]
    # 应用到当前组件
    m_theme.apply(widget)