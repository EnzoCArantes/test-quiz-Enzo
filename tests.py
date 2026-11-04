import pytest
from model import Question

@pytest.fixture
def five_choice_question():
    question = Question(title='q1', max_selections=5)

    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', False)
    question.add_choice('d', True)
    question.add_choice('e', False)

    return question

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_edge_cases_titles():
    question1 = Question(title='a')
    question2 = Question(title='a'*199)
    assert question1.id != None
    assert question2.id != None

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_question_with_invalid_edge_cases_points ():
    with pytest.raises(Exception):
        question = Question(title='q1', points=-1)
    with pytest.raises(Exception):
        question = Question(title='q1', points=0)
    with pytest.raises(Exception):
        question = Question(title='q1', points=101)    

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_remove_choice_by_invalid_id ():
    question = Question(title='q1')

    question.add_choice('a', False)

    choice = question.choices[0]

    with pytest.raises(Exception):
        question.remove_choice_by_id(choice.choice_id+1)

def test_remove_choice_by_valid_id ():
    question = Question(title='q1')

    question.add_choice('a', False)

    choice = question.choices[0]

    question.remove_choice_by_id(choice.id)

    assert len(question.choices) == 0
    
def test_remove_all_choices_with_empty_list ():
    question = Question(title='q1')

    previous_len = len(question.choices)

    question.remove_all_choices()

    assert previous_len == len(question.choices)

def test_remove_all_choices_with_many_choices ():
    question = Question(title='q1')

    question.add_choice('a', False)
    question.add_choice('b', False)
    question.add_choice('c', False)
    question.add_choice('d', True)
    question.add_choice('e', True)
    question.add_choice('f', True)

    question.remove_all_choices()

    assert len(question.choices) == 0

def test_set_correct_choice_changes_choice_correction_value ():
    question = Question(title='q1')

    question.add_choice('a', False)

    choice = question.choices[0]

    question.set_correct_choices([choice.id])

    assert choice.is_correct == True

def test_set_correct_choice_raises_exception_with_invalid_id ():
    question = Question(title='q1')

    question.add_choice('a', False)

    choice = question.choices[0]

    with pytest.raises(Exception):
        question.set_correct_choices([choice.id + 1])
    
def test_correct_selected_choices_returns_only_correct_choice ():
    question = Question(title='q1', max_selections=2)

    question.add_choice('a', True)
    question.add_choice('b', False)

    correct_ids = question.correct_selected_choices([question.choices[0].id, question.choices[1].id])

    assert len(correct_ids) == 1
    assert question.choices[0].id in correct_ids

def test_correct_selected_choices_raises_exception_when_too_many_choices ():
    question = Question(title='q1', max_selections=1)

    question.add_choice('a', True)
    question.add_choice('b', False)

    with pytest.raises(Exception):
        question.correct_selected_choices([question.choices[0].id, question.choices[1].id])

def test_correct_selected_choices_returns_no_choices_when_all_incorrect (five_choice_question):
    assert len(five_choice_question.correct_selected_choices([1, 3, 5])) == 0

def test_correct_selected_choices_raises_no_exception_with_empty_list (five_choice_question):
    assert len(five_choice_question.correct_selected_choices([])) == 0
    five_choice_question.remove_all_choices()
    assert len(five_choice_question.correct_selected_choices([])) == 0