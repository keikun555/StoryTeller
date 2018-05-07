"""
Kei Imada
20180506
Parser for stext files
"""
from STGraph import STGraph

def story_to_STGraph(filepath):
    contents = [[line.strip() for line in content.strip().split("\n")] for content in open(filepath, "r").read().split("\n\n")]
    storyline = {}
    content_num = 0
    for content in contents:
        # '0', 'hi', '2', '1 hello', '2 Are you ok?'
        content_id = content[0]
        text = content[1]
        num_choices = len(content)-2
        # try:
        #     num_choices = int(content[2])
        # except:
        #     num_choices = 0

        if content_id in storyline:
            raise Exception("Invalid fileformat for %s: content %d already mentioned\n%s" % (filepath, content_num, "\n".join(content)))

        storyline[content_id] = {}
        storyline[content_id]["text"] = text.replace("\\n", "\n")
        print storyline[content_id]["text"]
        choices = {}
        try:
            choices = dict([(content[i], content[i+1]) for i in range(2,len(content),2)])
        except:
            raise Exception("Invalid fileformat for %s: content %d could not get choices\n%s" % (filepath, content_num, "\n".join(content)))

        storyline[content_id]["choices"] = choices
        content_num += 1

    if "ST_start" not in storyline:
        raise Exception("Invalid fileformat for %s: root required with content id '0'" % (filepath))

    G = STGraph("ST_start", storyline["ST_start"]["text"])

    for content_id in storyline:
        G.add_node(content_id, storyline[content_id]["text"])
        for (choice,next_id) in storyline[content_id]["choices"].items():
            G.add_node(next_id, storyline[next_id]["text"])
            G.add_choice(content_id, next_id, choice)

    return G

if __name__ == "__main__":
    stext_to_STGraph("test_data.stext")

"""
{'1': {'text': 'How are you?', 'choices': {"I'm ok": '3'}}, '0': {'text': 'hi', 'choices': {'Are you ok?': '2', 'hello': '1'}}, '3': {'text': 'Thanks!', 'choices': {}}, '2': {'text': "I don't know", 'choices': {"Let's try again": '0', 'Ok': '3'}}}
"""
