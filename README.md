# gel-imaging-system
open source gel imager

* The detector consists of an raspberry hq camera, connected to a raspberry, that is mounted on top of a black box with an M6 screw and a nut.
* The black box is put over the light source, an blueBox™ S Transilluminator [^1].
* The image is then taken with a shell script that uses raspistill.
* The image can be analysed via ImageJ or, for instance, an python opencv solution.


![Imager](https://github.com/Georg-Auer/gel-imaging-system/blob/main/imager.jpeg)
![Imaging Workstation](https://github.com/Georg-Auer/gel-imaging-system/blob/main/imager-station.jpeg)
![First test image](https://github.com/Georg-Auer/gel-imaging-system/blob/main/gel_exposure1000000_2021_07_26_16_35.jpg)

- [x] Design
- [x] Laser cutting
- [x] Imaging script 
- [x] Image evaluation with Fiji[^2]

[^1]: https://www.minipcr.com/product/bluebox-dna-transilluminator/
[^2]: https://lukemiller.org/index.php/2010/11/analyzing-gels-and-western-blots-with-image-j/