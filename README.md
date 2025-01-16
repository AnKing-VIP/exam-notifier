## Exam Notifier for Anki

![](./screenshots/notification.png)

Exam Notifier provides users with notifications that a card will appear after an upcoming exam date. This feature allows the user to determine how to answer the card (i.e. Again, Hard, Good, Easy) or determine if rescheduling the card is deemed necessary. For example, a user may struggle with a particular subject and despite their ability to answer the card correctly, that they would like to revist these cards on the days leading up to their exam.

Many of us use Anki to prepare for exams. Some of us use Anki to learn a language in preparation for a trip to another country. Exam Notifier will tell you which cards are set to reappear after your test date. For example, if my big exam is coming up in 27 days and the current card is set to reappear in 28 days, this addon will notify you of this fact and give you the option to reschedule that card to reappear sooner for further review(s).

### Table of Contents <!-- omit in toc -->

<!-- MarkdownTOC levels="1,2,3" -->

- [Exam Notifier for Anki](#exam-notifier-for-anki)
  - [Installation](#installation)
  - [Documentation](#documentation)
  - [Building](#building)
  - [Developing](#developing)
  - [Contributing](#contributing)
  - [License and Credits](#license-and-credits)
  - [Supporting this Project](#supporting-this-project)

<!-- /MarkdownTOC -->

### Installation

#### AnkiWeb <!-- omit in toc -->

The easiest way to install Exam Notifier is through [AnkiWeb](https://ankiweb.net/shared/info/599952588).

#### Manual installation <!-- omit in toc -->

Please click on the entry corresponding to your Anki version:

<details>

<summary><i>Anki 2.1</i></summary>

1. Make sure you have the [latest version](https://apps.ankiweb.net/#download) of Anki 2.1 installed. Earlier releases (e.g. found in various Linux distros) do not support `.ankiaddon` packages.
2. Download the latest `.ankiaddon` package from the [releases tab](https://github.com/ankingmed/exam-notifier/releases) (you might need to click on *Assets* below the description to reveal the download links)
3. From Anki's main window, head to *Tools* → *Add-ons*
4. Drag-and-drop the `.ankiaddon` package onto the add-ons list
5. Restart Anki

Video summary:

<img src="https://raw.githubusercontent.com/glutanimate/docs/master/anki/add-ons/media/ankiaddon-installation.gif" width=640>

</details>

### Documentation

For further information on the use of this add-on please check out [the description text](docs/description.md) for AnkiWeb.

### Building

To build Exam Notifier, you will need to have the latest development build of [Anki add-on builder](https://github.com/glutanimate/anki-addon-builder) installed, alongside Qt5 and Qt6 dependencies:

```bash
pip install --upgrade git+https://github.com/glutanimate/anki-addon-builder.git@v1.0.0-dev.1#egg=aab[qt5,qt6]
```

You also need have Node and [yarn](https://yarnpkg.com/getting-started/install) installed.

You can then proceed to build the add-on via:

    git clone https://github.com/ankingmed/exam-notifier.git
    cd exam-notifier
    make build

For more information on the build process please refer to [`aab`'s documentation](https://github.com/glutanimate/anki-addon-builder/#usage).

### Developing

You can run `make develop` to build into `/src/exam_notifier`, which you can then soft link from `addons21` directory.

Run `yarn dev`, and when you edit an existing ts/svelte file, the files are re-built automatically. (You may still need to restart Anki for the changes to take effect)

### Contributing

Contributions are welcome! Please review the [contribution guidelines](./CONTRIBUTING.md) on how to:

- Report issues
- File pull requests
- Support the project as a non-developer

### License and Credits

*Exam Notifier* is *Copyright © 2019-2022 [Aristotelis P.](https://glutanimate.com/) (Glutanimate)*

All credits for the original idea for this add-on go to to [The AnKing](https://www.ankingmed.com/).

Exam Notifier is free and open-source software. The add-on code that runs within Anki is released under the GNU AGPLv3 license, extended by a number of additional terms. For more information please see the [LICENSE](https://github.com/ankingmed/exam-notifier/blob/master/LICENSE) file that accompanied this program.

Please note that this program uses the [Libaddon](https://github.com/glutanimate/anki-libaddon/) library which comes with [its own additional terms extending the GNU AGPLv3 license](https://github.com/glutanimate/anki-libaddon/blob/master/LICENSE). You may only copy, distribute, or modify the present compilation of this program with Libaddon under the combined licensing terms specified by both licenses.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY.


----

### Supporting this Project

If you enjoy Exam Notifier, please consider supporting our work through one of the means below:

<hr>

#### Supporting AnKing <!-- omit in toc -->

<b>Please consider checking out our:</b>
<center><div style="vertical-align:middle;"><a href="https://www.theanking.com"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/AnKing/TheAnKing-New.png?raw=true"></a></div></center>

<center>&nbsp;<a href="https://www.facebook.com/ankingmed"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/FB.png?raw=true"></a>
<a href="https://www.instagram.com/ankingmed"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/Instagram.png?raw=true"></a>
<a href="https://www.youtube.com/theanking"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/YT.png?raw=true"></a>
<a href="https://www.tiktok.com/@ankingmed"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/TikTok.png?raw=true"></a>
<a href="https://www.twitter.com/ankingmed"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/Social/Twitter.png?raw=true"></a></center>

<div><center><a href="https://www.theanking.com/vip"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/AnKing/Patreon.jpg?raw=true"></a></center></div>



<div><center><a href="https://courses.theanking.com"><img src="https://raw.githubusercontent.com/AnKingMed/My-images/master/AnKing/MasteryCourse.png?raw=true"></a></center></div>

<hr>

#### Supporting Glutanimate <!-- omit in toc -->

<p align="center"><a href="https://www.patreon.com/glutanimate"><img src="https://glutanimate.com/logos/glutanimate_small.png"></a></p>

<p align="center">Make sure to check out my socials for the latest add-on updates and news:</p>

<p align="center"><a href="https://twitter.com/glutanimate"><img src="https://glutanimate.com/logos/twitter.svg" alt="Twitter bird">@Glutanimate</a>&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.youtube.com/c/glutanimate"><img src="https://glutanimate.com/logos/youtube.svg" alt="YouTube playbutton"> / Glutanimate</a>&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.instagram.com/glutanimate"><img src="https://glutanimate.com/logos/instagram.svg" alt="Instagram"> / @Glutanimate</a></p>

<p align="center">Lots of <b>exclusive add-ons</b> and other goodies also await on my Patreon page. Make sure to take a look!:</p>

<p align="center">
<a href="https://www.patreon.com/glutanimate" title="❤️ Support me on Patreon"><img src="https://glutanimate.com/logos/patreon_button.svg"></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</p>

<hr>
