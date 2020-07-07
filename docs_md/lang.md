<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

<link rel="stylesheet" href="https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css" type="text/css" />

<style>
    a.src-href {
        float: right;
    }
    p.attr {
        margin-top: 0.5em;
        margin-left: 1em;
    }
    p.func-header {
        background-color: gainsboro;
        border-radius: 0.1em;
        padding: 0.5em;
        padding-left: 1em;
    }
    table.field-table {
        border-radius: 0.1em
    }
</style># Language tools

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.tools.**indef_article**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>indef_article</b>(<i>word</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/lang.py#L3">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>word : <i>str</i></b>
<p class="attr">
    Word to which the indefinite article belongs.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>article : <i>str</i></b>
<p class="attr">
    <code>'an'</code> if <code>word</code> starts with a vowel, or <code>'a'</code> otherwise, followed by the word.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock.tools import indef_article

[indef_article(fruit) for fruit in ('apple','banana')]
```

Out:

```
['an apple', 'a banana']
```

##hemlock.tools.**join**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>join</b>(<i>joiner, *items</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/lang.py#L32">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>joiner : <i>str</i></b>
<p class="attr">
    Joins the first n-1 items with the last item, e.g. <code>'and'</code>.
</p>
<b>*items : <i>str</i></b>
<p class="attr">
    Items to join.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>joined : <i>str</i></b>
<p class="attr">
    Joined items.
</p></td>
</tr>
    </tbody>
</table>

####Examples

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

##hemlock.tools.**plural**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>plural</b>(<i>n, singular, plural=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/lang.py#L73">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>n : <i>int</i></b>
<p class="attr">
    Number.
</p>
<b>singular : <i>str</i></b>
<p class="attr">
    The singular form of the word.
</p>
<b>plural : <i>str or None, default=None</i></b>
<p class="attr">
    The plural form of the word. If <code>None</code>, the plural form is assumed to be the singular + 's'.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>word : <i>str</i></b>
<p class="attr">
    The singular form if number is 1, plural form otherwise.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock.tools import plural

['{} {}'.format(n, plural(n, 'cat')) for n in range(0,3)]
```

Out:

```
['0 cats', '1 cat', '2 cats']
```

##hemlock.tools.**pronouns**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>pronouns</b>(<i>person, singular, gender=None, pfx=''</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/lang.py#L108">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>person : <i>int</i></b>
<p class="attr">
    <code>1</code>, <code>2</code>, or <code>3</code> for first, second, or third person.
</p>
<b>singular : <i>bool</i></b>
<p class="attr">
    <code>True</code> for singular, <code>False</code> for plural.
</p>
<b>gender : <i>str or None, default=None</i></b>
<p class="attr">
    <code>'male'</code>, <code>'female'</code>, <code>'neuter'</code>, or <code>'epicene'</code>. Required for third person singular pronouns.
</p>
<b>pfx : <i>str, default=''</i></b>
<p class="attr">
    Prefix for dictionary keys. Use this to distinguish between multiple entities in a single string.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>pronouns : <i>dict</i></b>
<p class="attr">
    Mapping of pronoun keys to pronouns. Pronoun keys are <code>'subject'</code>, <code>'object'</code>, <code>'dep_poss'</code> (dependent possessive), <code>'indep_poss'</code>, (indepedent possessive), <code>'reflex'</code> (reflexive).
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock.tools import pronouns

string = '''
{A_subject} said hello to {B_object} as {B_subject} was walking
{B_dep_poss} neighbor's dog. 'Is that dog {B_indep_poss}?', {A_subject}
thought to {A_reflex}.
'''
string.format(
    **pronouns(3, True, 'male', pfx='A_'),
    **pronouns(3, True, 'female', pfx='B_')
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
    **pronouns(3, True, 'female', pfx='A_'),
    **pronouns(3, True, 'male', pfx='B_')
)
```

Out:

```
she said hello to him as he was walking
his neighbor's dog. 'Is that dog his?', she
thought to herself.
```