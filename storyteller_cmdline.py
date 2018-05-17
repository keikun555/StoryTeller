"""
Kei Imada
20180506
A storyteller implemented in commandline
"""
from STParser import story_to_STGraph
from STGraph import STGraph
import networkx as nx
import os

STORY_FILEPATH = "static/stories/heyjude.story"

def main():
    G = story_to_STGraph(STORY_FILEPATH)
    G.visualize(show_story_text=False, show_choice_texts=False)
    keyboard_input = ""
    os.system('clear')
    print G.get_current()
    while(len(G.get_choices()) > 0 and keyboard_input not in ["exit", "quit"]):
        choices = G.get_choices()
        print_choices(choices)
        keyboard_input = raw_input("choice: ").lower()
        os.system('clear')
        if keyboard_input.isdigit():
            c_id = int(keyboard_input)
            if(c_id < 0 or c_id >= len(choices)):
                print "please enter a valid choice id"
                print G.get_current()
            else:
                G.choose(choices[c_id])
                print G.get_current()
        else:
            if keyboard_input in ["exit", "quit"]:
                print "aw i hope you come again"
            else:
                print "please enter a valid choice id"
                print G.get_current()



def print_choices(choice_list):
    for (c_id, text) in zip(range(len(choice_list)), choice_list):
        print "%s: %s" % (c_id, text)

if __name__ == '__main__':
    main()
