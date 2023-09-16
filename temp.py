import random
import time


def main():
    # helps the user with rules and hints
    args = input("Enter '-help' for rules and hints: ").split()
    if len(args) != 0 and args[0].lower() == "-help":
        help_menu()
        return

    # starts the game
    print("You are in a cube-shaped room with a door on three of the walls.")
    print("You have no idea how you got here.")
    print("You just know you need to leave as soon as possible.")
    print("Choose a door.\n")

    # main 3 doors
    print("----------------")
    print("  Door 1")
    print("  Door 2")
    print("  Door 3")
    print("----------------")

    # input from the user to choose a door
    door_num = int(input())

    # if entered door 1, then mathGame1, mathGame2, and coinFlip minigames will play
    if door_num == 1:
        math_game1()
    # if you enter door 2, then the Memory and typingMinigame minigames will play
    elif door_num == 2:
        memory()
    # if you enter door 3, then trivia and rockPaperScissor minigames will play
    elif door_num == 3:
        trivia()


# displays the rules and hints
def help_menu():
    print("Help menu: Enter a 1, 2, or 3 to enter a door.")
    print("Rules: Enter a number to start the game.")
    print("You will need to enter complete sentences, letters, or numbers to proceed through the game.")
    print("Some games will require luck and no skill.")


# Example minigame functions (you can define these as needed)
def math_game1():
    # Implement your math game logic here
    pass


def memory():
    # Implement your memory game logic here
    pass


def trivia():
    # Implement your trivia game logic here
    pass


if __name__ == "__main__":
    main()