"""Create experiment as a web application"""

from survey import Start

from hemlock import create_app

settings = {
    'start': Start
    }

app = create_app(settings)
    
if __name__ == '__main__':
    app.run()
    
import hemlock_shell