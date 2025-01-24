---
id: markdown
---

A file containing all the markdown Pike should support.
This is taken from: https://www.markdownguide.org/basic-syntax/

Headings:

# Heading level 1
## Heading level 2
### Heading level 3
#### Heading level 4 
##### Heading level 5 
###### Heading level 6


Other heading styles:

Heading level 1
===============

Heading level 2
---------------



Paragraphs:
I really like using Markdown.

I think I'll use it to format all of my documents from now on. 


Line break:
This is the first line.
And this is the second line. 

Bold:
I just love **bold text**.
I just love __bold text__.


Italic:
Italicized text is the *cat's meow*.
Italicized text is the _cat's meow_.


Bold and Italic:
This text is ***really important***.
This text is ___really important___.
This text is __*really important*__.
This text is **_really important_**.


Blockquotes: (TODO)
> Dorothy followed her through many of the beautiful rooms in her castle.


Blockquotes with multiple paragraphs: (TODO)
> Dorothy followed her through many of the beautiful rooms in her castle.
>
> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.


Nested blockquotes: (TODO)
> Dorothy followed her through many of the beautiful rooms in her castle.
>
>> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.


Blockquotes with other elements: (TODO)
> #### The quarterly results look great!
>
> - Revenue was off the chart.
> - Profits were higher than ever.
>
>  *Everything* is going according to **plan**.


Ordered lists:
1. First item
2. Second item
3. Third item
4. Fourth item 

Different markdown, same list result:
1. First item
1. Second item
1. Third item
1. Fourth item


Unordered lists:
- First item
- Second item
- Third item
- Fourth item 

Different markdown, same list result:
* First item
* Second item
* Third item
* Fourth item 

Different markdown, same list result:
+ First item
+ Second item
+ Third item
+ Fourth item 


Nested lists:
1. First item
2. Second item
3. Third item
    1. Indented item
    2. Indented item
4. Fourth item 

- First item
- Second item
- Third item
  - Indented item
  - Indented item
- Fourth item 


Inline code:
At the command prompt, type `nano`.


Escaped code:
Pike does not support the following syntax example:
\`\`Use \`code\` in your Markdown file.\`\`

If you wish to use backticks without making inline code blocks, use a backslash. `\`


Horizontal rules:

One type:

---

Second type:

***

Third type:

___


Links:
My favorite search engine is [Duck Duck Go](https://duckduckgo.com).


Titled links: (Not supported at this time)
My favorite search engine is [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy").


Quick links / emails:
<https://www.markdownguide.org>
<fake@example.com>


Reference-s tyle links: (TODO)
Usage:
- [hobbit-hole][1]
Ref:
- [1]: https://en.wikipedia.org/wiki/Hobbit#Lifestyle
- [1]: https://en.wikipedia.org/wiki/Hobbit#Lifestyle "Hobbit lifestyles"
- [1]: https://en.wikipedia.org/wiki/Hobbit#Lifestyle 'Hobbit lifestyles'
- [1]: https://en.wikipedia.org/wiki/Hobbit#Lifestyle (Hobbit lifestyles)
- [1]: <https://en.wikipedia.org/wiki/Hobbit#Lifestyle> "Hobbit lifestyles"
- [1]: <https://en.wikipedia.org/wiki/Hobbit#Lifestyle> 'Hobbit lifestyles'
- [1]: <https://en.wikipedia.org/wiki/Hobbit#Lifestyle> (Hobbit lifestyles)


Images:
![My cat!](images/cat.jpg "Its my cat")


Linked images: (TODO)
[![An old rock in the desert](/assets/images/shiprock.jpg "Shiprock, New Mexico by Beau Rogers")](https://www.flickr.com/photos/beaurogers/31833779864/in/photolist-Qv3rFw-34mt9F-a9Cmfy-5Ha3Zi-9msKdv-o3hgjr-hWpUte-4WMsJ1-KUQ8N-deshUb-vssBD-6CQci6-8AFCiD-zsJWT-nNfsgB-dPDwZJ-bn9JGn-5HtSXY-6CUhAL-a4UTXB-ugPum-KUPSo-fBLNm-6CUmpy-4WMsc9-8a7D3T-83KJev-6CQ2bK-nNusHJ-a78rQH-nw3NvT-7aq2qf-8wwBso-3nNceh-ugSKP-4mh4kh-bbeeqH-a7biME-q3PtTf-brFpgb-cg38zw-bXMZc-nJPELD-f58Lmo-bXMYG-bz8AAi-bxNtNT-bXMYi-bXMY6-bXMYv)


Escaped characters:
\* Without the backslash, this would be a bullet in an unordered list.

---

Extended syntax
Comes from here: https://www.markdownguide.org/extended-syntax/

Tables:
| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |

Table alignment: (left, middle, right)
| Aligned   | Description | Test Text |Normal   |
| :---      |    :----:   |      ---: | ---     |
| Left      | Middle      | Right     | Regular |

Table formatting:
| Formatting      | Here |
| ----------- | ----------- |
| *Italic*    | `Inline` |
| **Bold**   | Nothing        |


Code: (no syntax highlighting)
```
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```


Footnotes:
Here's a simple footnote,[^1] and here's a longer one.[^bignote]

[^1]: This is the first footnote.

[^bignote]: Here's one with multiple paragraphs and code.

    Indent paragraphs to include them in the footnote.

    \`{ my code }\` TODO Fix this code block once implemented

    Add as many paragraphs as you like.


Heading IDs:
### My Great Heading { #custom-id }

Definition lists: (not supported)

First Term
: This is the definition of the first term.

Second Term
: This is one definition of the second term.
: This is another definition of the second term.


Strikethrough:
~~The world is flat.~~ We now know that the world is round.


Task lists:
- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media


Highlighting:
I need to highlight these ==very important words==.


Subscript:
H~2~O (Should have 2 sub-scripted)

Superscript:
X^2^ (Should have 2 super-scripted)