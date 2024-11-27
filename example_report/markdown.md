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

1. First item
1. Second item
1. Third item
1. Fourth item


Unordered lists:
- First item
- Second item
- Third item
- Fourth item 

* First item
* Second item
* Third item
* Fourth item 

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
``Use `code` in your Markdown file.``


Horizontal rules:

---

***

___


Links:
My favorite search engine is [Duck Duck Go](https://duckduckgo.com).


Titled links:
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
![My cat!](/images/cat.jpg "Its my cat")


Linked images: (TODO)
[![An old rock in the desert](/assets/images/shiprock.jpg "Shiprock, New Mexico by Beau Rogers")](https://www.flickr.com/photos/beaurogers/31833779864/in/photolist-Qv3rFw-34mt9F-a9Cmfy-5Ha3Zi-9msKdv-o3hgjr-hWpUte-4WMsJ1-KUQ8N-deshUb-vssBD-6CQci6-8AFCiD-zsJWT-nNfsgB-dPDwZJ-bn9JGn-5HtSXY-6CUhAL-a4UTXB-ugPum-KUPSo-fBLNm-6CUmpy-4WMsc9-8a7D3T-83KJev-6CQ2bK-nNusHJ-a78rQH-nw3NvT-7aq2qf-8wwBso-3nNceh-ugSKP-4mh4kh-bbeeqH-a7biME-q3PtTf-brFpgb-cg38zw-bXMZc-nJPELD-f58Lmo-bXMYG-bz8AAi-bxNtNT-bXMYi-bXMY6-bXMYv)


Escaped characters:
\* Without the backslash, this would be a bullet in an unordered list.