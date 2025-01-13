# ui/scrollarea_styles.py

scrollarea_styles = """
    QScrollArea {
        background-color: #2f2f2f;  
        border: 1px solid #444444;   
        border-radius: 12px;          
        padding: 10px;               
    }

    QScrollBar:vertical {
        background-color: #3a3a3a;   
        width: 12px;                 
        border-radius: 12px;         
        margin: 3px;                 
    }

    QScrollBar:horizontal {
        background-color: #3a3a3a;   
        height: 12px;                
        border-radius: 12px;         
        margin: 3px;                 
    }

    QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #555555, stop: 1 #888888); 
        border-radius: 12px;         
        min-height: 20px;            
        min-width: 20px;             
        border: 2px solid #444444;   
    }

    QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #777777, stop: 1 #aaaaaa);  
        border: 2px solid #666666;   
    }

    QScrollBar::handle:vertical:pressed, QScrollBar::handle:horizontal:pressed {
        background-color: #999999;   
        border: 2px solid #777777;   
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    background: none;            
    }

    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
    QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
        background: none;            
    }

    
    QScrollBar:vertical:hover, QScrollBar:horizontal:hover {
        background-color: #444444;   
    }

    
    QScrollBar::vertical:disabled, QScrollBar::horizontal:disabled {
        background-color: transparent; 
    }

    
    QScrollArea::corner {
        background-color: transparent; 
    }
"""
