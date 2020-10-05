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
</style># Comprehension check

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.tools.**comprehension_check**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>comprehension_check</b>(<i>instructions, checks, attempts=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/comprehension.py#L8">[source]</a>
</p>

A comprehension check consists of 'instruction' pages followed by 'check'
pages. The data of all questions in a check page must evaluate to `True`
to pass the check. When a participant fails a check, he is brought back to
the first instructions page.

Participants only have to pass each check once. For example, suppose there
are two checks, A and B. The participant passes check A but fails check B.
He is brought back to the first page of the instructions. After rereading
the instructions, he is brought directly to check B, skipping check A.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>instructions : <i>hemlock.Page or list of hemlock.Page</i></b>
<p class="attr">
    Instruction page(s).
</p>
<b>checks : <i>hemlock.Page or list of hemlock.Page</i></b>
<p class="attr">
    Check page(s).
</p>
<b>attempts : <i>int or None, default=None</i></b>
<p class="attr">
    Number of attempts allotted. Participants are allowed to proceed with the survey after exceeding the maximum number of attempts. If <code>None</code>, participants must pass the comprehension check before continuing the survey.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>pages : <i>list of hemlock.Page</i></b>
<p class="attr">
    List of instructions pages + check pages.
</p></td>
</tr>
    </tbody>
</table>

####Notes

This function adds a `hemlock.Submit` function to each check page. This
must be the last submit function of each check page.

####Examples

We have two files in our root directory. In `survey.py`:

```python
from hemlock import Branch, Page, Label, Input, Submit as S, route
from hemlock.tools import comprehension_check

@route('/survey')
def start():
    return Branch(
        *comprehension_check(
            instructions=Page(
                Label('<p>Here are some instructions.</p>')
            ),
            checks=Page(
                Input(
                    '<p>Enter "hello world" or you... shall not... PASS!</p>',
                    submit=S.match('hello world')
                )
            )
        ),
        Page(
            Label('<p>You passed the comprehension check!</p>'),
            terminal=True
        )
    )
```

In `app.py`:

```python
import survey

from hemlock import create_app

app = create_app()

if __name__ == '__main__':
    from hemlock.app import socketio
    socketio.run(app, debug=True)
```

Run the app with:

```
$ python app.py # or python3 app.py
```

Open your browser to <http://localhost:5000/>.