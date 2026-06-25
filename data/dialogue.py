from data.ascii import asciis

king = {
    "name": "The King",
    "sprite": asciis["king"],
    "dialogue": {
        "default": [
            "Good day, {PLAYER_NAME}."
        ],
        "tutorial": [
            "Ah, hello {PLAYER_NAME}! I have been expecting you.",
            "I am The King.",
            "I welcome you to Naokorius. These lands have grown dangerous as of late.",
            "Here in Naokorius you type in your commands.",
            "You will see a menu with all of your options. You either type in the corresponding number or the option.",
            "Keep an eye on your HP. Once it hits zero, you're dead.",
            "Your MP fuels your abilities. Rest at a campfire to recover both your MP and HP.",
            "As you defeat enemies, do quests and finish areas you will grow stronger and level up.",
            "Speak to other people to get quests or receive items.",
            "Now wake up, {PLAYER_NAME}. Get me out of your simple mind and do something with your worthless life.",
        ],
    }
}