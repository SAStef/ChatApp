set_theme_button = """
    QPushButton {
        background-color: #34495E;  /* Slightly lighter blue background */
        color: #FFFFFF;
        border: 2px solid #5D6D7E;  /* Subtle lighter border */
        max-width: 80px;  /* Smaller button width */
        max-height: 25px;  /* Smaller button height */
        border-radius: 8px;  /* Rounded corners */
        padding: 4px 8px;  /* Less padding */
        font-size: 11px;  /* Smaller font size */
        font-weight: normal;  /* Less bold */
        text-align: center;
        background: #34495E;
    }
    QPushButton:hover {
        background-color: #5D6D7E;  /* Lighter blue on hover */
        border: 2px solid #85929E;  /* Lighter border */
    }
    QPushButton:pressed {
        background-color: #34495E;  /* Keep the background same when pressed */
        border: 2px solid #5D6D7E;  /* Same border as default */
    }
"""
