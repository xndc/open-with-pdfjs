# Open With PDF.js

This is a tiny "application" for macOS that opens PDF files in your default browser, using Mozilla's [PDF.js](https://mozilla.github.io/pdf.js/) viewer.

Using PDF.js on Safari or Chrome is, in my humble opinion, the best option for viewing PDFs on macOS at the moment. Not because PDF.js is good, but because the competition is so bad:

* Preview renders PDFs with extreme amounts of blur applied - see [Apple Support Forums](https://discussions.apple.com/thread/8226552), [MacRumors](https://forums.macrumors.com/threads/pdfs-and-preview-—-why-so-blurry.2145687/), [Reddit #1](https://old.reddit.com/r/MacOS/comments/8tpdg9/is_blurry_pdf_rendering_in_preview_fixed_in/), [Reddit #2](https://www.reddit.com/r/apple/comments/72lxjx/macos_high_sierra_blurry_pdfs_in_preview/), [StackExchange #1](https://apple.stackexchange.com/questions/357194/how-to-make-preview-render-pdf-docs-with-crisp-fonts-on-macbook-air-without-ret?rq=1), [StackExchange #2](https://apple.stackexchange.com/questions/347981/blurry-pdf-in-preview-safari-on-osx-mojave).
* Every other application based on PDFKit (e.g. Safari, Skim) has the same issue.
* Chrome's PDF reader does not remember scroll positions ([issue 65244](https://bugs.chromium.org/p/chromium/issues/detail?id=65244)).
* Firefox has egregious power management issues on Macs.
* Foxit Reader has an awful interface, broken controls and is proprietary to boot.
* Adobe Reader is 200 MiB of borderline malware that expects me to run an installer.

Since none of the options appealed to me very much, I wrote this script.

## Download

Just download and unpack [PDF Viewer.zip](https://github.com/xndc/open-with-pdfjs/raw/master/PDF%20Viewer.zip) from this repository.

Place the app bundle inside your Applications directory. Right-click it, hold Cmd and click "Open". Confirm that you do want Gatekeeper to let you run it.

This should open the PDF.js viewer in your browser, featuring a red banner complaining about not being able to read a file. This is fine. You can drop a PDF file onto the browser window to try it out, or just close the tab.

After you launch it for the first time, the tool should show up in the Finder's "Open With" menu. If it doesn't, you can just click "Other" and find it yourself.

If you want to make it your default PDF viewer, right-click any PDF file, click "Get Info", select it out of the "Open With" menu and click "Change All". You can do the same procedure with Preview.app to revert this.

## Details

**Q: How fast is it?**  
A: Scrolling is quite janky. Pages can take a few hundred milliseconds to load when scrolling or skipping to another section. It's strictly inferior to both Preview and PDFium.

**Q: How lightweight is it?**  
A: Under Safari on my 2015 MacBook Air, it uses between 100 to 200 MiB of memory on non-trivial documents and uses about 30% of CPU time (across all cores) while scrolling. It's not going to win any awards.

**Q: So it's not good for battery life?**  
A: I haven't used it long enough to tell, but it doesn't seem to have any significant battery impact despite being quite heavyweight.

**Q: Does it render PDFs without blur?**  
A: Mostly. Images are rendered with slightly more blur in Safari than in Chrome, for some reason that I haven't been able to pin down yet. It's nowhere near as bad as Preview, though!


## Building

The application bundle is built with [Platypus](https://sveinbjorn.org/platypus). This repository includes both a copy of Platypus and the "profile" used to create the bundle. Just drag and drop it onto Platypus.app to get started, and change whatever settings you want to change.

In case the profile doesn't work for some reason, here's how it was generated:

1. Drag `Launcher.py` into the "Script Path" field.
2. Give the app a name, like "PDF Viewer".
3. Click on the "Custom Icon" gear button, choose "Select Image File" and browse to `Logo.png`.
4. Set "Interface" to "None".
5. Untick "Remain running after execution", "Run in background" and "Run with root privileges".
6. Tick "Accept dropped items" and click "Settings". A modal dialog will open.
7. Tick "Accept dropped files".
8. Delete the default UTIs and add a single one: `com.adobe.pdf`.
9. Click "Select document icon", then press Cmd-Shift-G to bring up the "Go to folder" dialog.
10. Paste `/Applications/Preview.app/Contents/Resources/pdf.icns` into the text box and press Enter.
11. The "pdf.icns" file should show up. Click "Open".
12. Click "Apply" to close the Settings dialog.
13. Drag the `pdfjs-dist` folder into the "Bundled Files" list.
14. Click "Create App" and choose where to save it.

The `pdfjs-dist` directory contains Mozilla's official pre-built version of PDF.js, version 2.0.943, with only a couple of changes:

* Inside `web/viewer.js`, the reference to `compressed.tracemonkey-pldi-09.pdf` has been replaced with `/pdf`, the endpoint at which the target PDF file is hosted. (See below.)
* The test PDF file in the package has been deleted.
* The various .map files in the package have been deleted.

You should be able to upgrade PDF.js easily once new releases come out. Just modify `viewer.js` and rebuild the app.

## How it works

The procedure is rather awful, but I can't think of any simpler solutions at the moment.

1. The executable generated by Platypus runs the `Launcher.py` script.
2. `Launcher.py` starts a web server on 127.0.0.1:10733, serving the PDF.js viewer and any given PDF file.
3. Your default web browser is used to open the hosted "website".
4. PDF.js loads itself, then starts downloading the PDF file given to the script (if any).
4. The server shuts down a couple of seconds after the download finishes (or fails).

## License and Credits

The "PDF Viewer.app" bundle is available under the [Apache License, version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).

[PDF.js](https://mozilla.github.io/pdf.js/) has [multiple authors](https://github.com/mozilla/pdf.js/blob/master/AUTHORS) and is available under the [Apache License, version 2.0](https://github.com/mozilla/pdf.js/blob/master/LICENSE).  
[Platypus](https://sveinbjorn.org/platypus) is &copy; Sveinbjorn Thordarson and available under the [three-clause BSD license](https://sveinbjorn.org/bsd_license).  
The `Launcher.py` script is available under the zlib License.