"""# Language tools"""

def indef_article(word):
    """
    Parameters
    ----------
    word : str
        Word to which the indefinite article belongs.

    Returns
    -------
    article : str
        `'an'` if `word` starts with a vowel, or `'a'` otherwise, followed 
        by the word.

    Examples
    --------
    ```python
    from hemlock.tools import indef_article

    [indef_article(fruit) for fruit in ('apple','banana')]
    ```

    Out:

    ```
    ['an apple', 'a banana']
    ```
    """
    return 'an '+word if word[0] in 'aeiou' else 'a '+word

def join(joiner, *items):
    """
    Parameters
    ----------
    joiner : str
        Joins the first n-1 items with the last item, e.g. `'and'`.

    \*items : str
        Items to join.

    Returns
    -------
    joined : str
        Joined items.

    Examples
    --------
    ```python
    from hemlock.tools import join

    print(join('and', 'world', 'sun'))
    print(join('or', 'world', 'sun', 'moon'))
    ```

    Out:

    ```
    world and sun
    world, sun, or moon
    ```
    """
    if not items:
        return ''
    if len(items) == 1:
        return str(items[0])
    if len(items) == 2:
        return '{} {} {}'.format(items[0], joiner, items[1])
    string = ', '.join([str(i) for i in items[:-1]])
    string += ', {} {}'.format(joiner, str(items[-1]))
    return string

def plural(n, singular, plural=None):
    """
    Parameters
    ----------
    n : int
        Number.

    singular : str
        The singular form of the word.

    plural : str or None, default=None
        The plural form of the word. If `None`, the plural form is assumed to
        be the singular + 's'.

    Returns
    -------
    word : str
        The singular form if number is 1, plural form otherwise.

    Examples
    --------
    ```python
    from hemlock.tools import plural

    ['{} {}'.format(n, plural(n, 'cat')) for n in range(0,3)]
    ```

    Out:

    ```
    ['0 cats', '1 cat', '2 cats']
    ```
    """
    return singular if n==1 else (plural or singular+'s')

def pronouns(person, singular, gender=None, pfx=''):
    """
    Parameters
    ----------
    person : int
        `1`, `2`, or `3` for first, second, or third person.

    singular : bool
        `True` for singular, `False` for plural.

    gender : str or None, default=None
        `'male'`, `'female'`, `'neuter'`, or `'epicene'`. Required for third 
        person singular pronouns.

    pfx : str, default=''
        Prefix for dictionary keys. Use this to distinguish between multiple
        entities in a single string.

    Returns
    -------
    pronouns : dict
        Mapping of pronoun keys to pronouns. Pronoun keys are `'subject'`, 
        `'object'`, `'dep_poss'` (dependent possessive), `'indep_poss'`,
        (indepedent possessive), `'reflex'` (reflexive).

    Examples
    --------
    ```python
    from hemlock.tools import pronouns

    string = '''
    {A_subject} said hello to {B_object} as {B_subject} was walking 
    {B_dep_poss} neighbor's dog. 'Is that dog {B_indep_poss}?', {A_subject}
    thought to {A_reflex}.
    '''
    string.format(
    \    **pronouns(3, True, 'male', pfx='A_'),
    \    **pronouns(3, True, 'female', pfx='B_')
    )
    ```

    Out:

    ```
    he said hello to her as she was walking 
    her neighbor's dog. 'Is that dog hers?', he
    thought to himself.
    ```

    In:

    ```python
    string.format(
    \    **pronouns(3, True, 'female', pfx='A_'),
    \    **pronouns(3, True, 'male', pfx='B_')
    )
    ```

    Out:

    ```
    she said hello to him as he was walking 
    his neighbor's dog. 'Is that dog his?', she
    thought to herself.
    ```
    """
    selected = pronouns_[person]['singular' if singular else 'plural']
    selected = selected[gender] if person == 3 and singular else selected
    return {str(pfx)+key: val for key, val in selected.items()}

pronouns_ = {
    1: {
        'singular': {
            'subject': 'I',
            'object': 'me',
            'dep_poss': 'my',
            'indep_poss': 'mine',
            'reflex': 'myself',
        },
        'plural': {
            'subject': 'we',
            'object': 'us',
            'dep_poss': 'our',
            'indep_poss': 'ours',
            'reflex': 'ourselves',
        }
    },
    2 : {
        'singular': {
            'subject': 'you',
            'object': 'you',
            'dep_poss': 'your',
            'indep_poss': 'yours',
            'reflex': 'yourself',
        },
        'plural': {
            'subject': 'you',
            'object': 'you',
            'dep_poss': 'your',
            'indep_poss': 'yours',
            'reflex': 'yourselves',
        },
    },
    3: {
        'singular': {
            'male': {
                'subject': 'he',
                'object': 'him',
                'dep_poss': 'his',
                'indep_poss': 'his',
                'reflex': 'himself',
            },
            'female': {
                'subject': 'she',
                'object': 'her',
                'dep_poss': 'her',
                'indep_poss': 'hers',
                'reflex': 'herself',
            },
            'neuter': {
                'subject': 'it',
                'object': 'it',
                'dep_poss': 'its',
                'indep_poss': 'its',
                'reflex': 'itself',
            },
            'epicene': {
                'subject': 'they',
                'object': 'them',
                'dep_poss': 'their',
                'indep_poss': 'theirs',
                'reflex': 'themself',
            }
        },
        'plural': {
            'subject': 'they',
            'object': 'them',
            'dep_poss': 'their',
            'indep_poss': 'theirs',
            'reflex': 'themselves',
        }
    }
}