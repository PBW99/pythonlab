import sys
import click
from PyInquirer import prompt, print_json
from subprocess import call


@click.group(invoke_without_command=True)
def root():
    if len(sys.argv) == 1:
        interactive()


@root.command()
@click.option('--count', default=1, help='Number')
@click.option('--name')
def create(count, name):
    print(f'[call] create {count} {name}')


@root.command()
@click.option('--name')
def read(name):
    print(f'[call] read {name}')


@root.command()
@click.option('--name')
def delete(name):
    print(f'[call] delete { name}')


def interactive():
    command_answers = prompt(
        {'type': 'list',
         'name': 'command',
         'message': 'command',
         'choices': root.commands})
    command_func = globals()[command_answers["command"]]

    para = create.params[0]
    para.type

    option_questions = []
    for p in command_func.params:
        question = {'type': 'input',
                    'name': p.name,
                    'message': p.name}
        if p.default is not None:
            question['default'] = str(p.default)

        option_questions.append(question)
    option_answers = prompt(option_questions)
    call_args = ["python", sys.argv[0], command_answers["command"]]
    for p in command_func.params:
        call_args.append(f'--{p.name}')
        call_args.append(option_answers[p.name])

    call(call_args)


if __name__ == '__main__':
    root()
