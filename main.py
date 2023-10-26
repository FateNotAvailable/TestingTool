from colorama import init, Fore
from PyInquirer import prompt, style_from_dict, Token, Separator
from difflib import SequenceMatcher
import os
import platform
init()

# Define questions / answers here
questions = [
    ("Ako určujeme veľkosť fyzikálnej veličiny?", "meraním"),
    ("Čo sa nachádza v obale atómu?", "elektrón"),
    ("Aká je jednotka elektrickej kapacity?", "farad"),
    ("Aká je jednotka elektrického prúdu?", "ampér"),
    ("Čo vyjadruje kapacita?", "nahromadiť elektrický náboj"),
    ("Čo znamená slovo \"dielektrikum\"?", "izolant"),
    ("Ako označujeme elektrické napätie?", "V"),
    ("Čo znamená DC (Direct Current)?", "jednosmerný prúd"),
    ("Aký prístroj merá Elektrické napätie?", "voltmeter"),
    ("Ako zapájame ampérmeter do obvodu?", "sériovo")
]

# Initiate all answers as "No Answer"
answers = {key: "No Answer" for key, _ in questions}

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
    Token.Icon: ''
})


def clear_console():
    os_name = platform.system().lower()
    if os_name.startswith('win'):
        os.system('cls')
    elif os_name.startswith('linux') or os_name.startswith('darwin'):
        os.system('clear')
    else:
        print("Unsupported operating system. Unable to clear console.")


def main():
    clear_console()

    global answers

    options = [{
        'type': 'list',
        'message': 'Select question',
        'name': 'options',
        'choices': [
            f"{question} | {answers.get(question, 'Not Answered Yet')}" for question, _ in questions
        ]
    }]
    
    options[0]['choices'].extend([
        Separator(),
        f"Finish / Evaluate Results"
    ])

    selected = prompt(options, style=style)

    if selected['options'] == options[0]['choices'][-1]:
        finish()
        return

    answer_question(selected['options'].split(" | ")[0])
    return


def answer_question(question):
    clear_console()

    global answers

    answer = input(f"{Fore.BLUE}Q: {question}{Fore.WHITE}\nA: ")
    if not answer:
        main()

    answers[question] = answer
    main()


def finish():
    clear_console()

    correct_answer_count = 0

    def correct(question, answer):
        print(f"{Fore.BLUE}{question}: {Fore.GREEN}{answer}{Fore.WHITE}")


    def incorrect(question, answer):
        print(f"{Fore.BLUE}{question}: {Fore.RED}{answer}{Fore.WHITE}")

    for question, correct_answer in questions:
        user_answer = answers.get(question, "")
        if not user_answer:
            incorrect(question, "No Answer was provided")

        seq_matcher = SequenceMatcher(None, correct_answer.lower(), user_answer.lower())

        # Get the similarity ratio
        similarity_ratio = seq_matcher.ratio()

        if similarity_ratio >= 0.8:
            correct(question, user_answer)
            correct_answer_count += 1
            continue

        incorrect(question, user_answer)
    

    print(Separator())
    percentage = round(correct_answer_count/len(questions), 3) * 100

    stat_color = Fore.RED
    if percentage > 75:
        stat_color = Fore.GREEN

    print(f"Score: {stat_color}{correct_answer_count}/{len(questions)}{Fore.WHITE} | {stat_color}{percentage}%{Fore.WHITE}")
    input("Press [Enter] to exit")
    exit()



if __name__ == "__main__":
    main()
