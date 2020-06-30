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
    <code>'an'</code> if <code>word</code> starts with a vowel, <code>'a'</code> otherwise.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**plural**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>plural</b>(<i>n, singular, plural=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/lang.py#L17">[source]</a>
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



##hemlock.tools.**pronouns**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>pronouns</b>(<i>person, singular, gender=None, pfx=''</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/lang.py#L38">[source]</a>
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

