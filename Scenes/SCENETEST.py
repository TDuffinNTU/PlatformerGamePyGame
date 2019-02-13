from Scenes.StackStateMachine import *
from Scenes.MainMenu import *

def main():
    s = StateMachine(MainMenu)
    s.run()

if __name__ == "__main__":
    main()