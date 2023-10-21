"""
Luminous Efficiency Functions Spectral Distributions
====================================================

Defines the luminous efficiency functions computation related objects.

References
----------
-   :cite:`Wikipedia2005d` : Wikipedia. (2005). Mesopic weighting function.
    Retrieved June 20, 2014, from
    http://en.wikipedia.org/wiki/Mesopic_vision#Mesopic_weighting_function
"""

from __future__ import annotations

from colour.colorimetry import (
    SDS_LEFS_PHOTOPIC,
    SDS_LEFS_SCOTOPIC,
    SpectralDistribution,
    SpectralShape,
)
from colour.colorimetry.datasets.lefs import DATA_MESOPIC_X
from colour.hints import ArrayLike, Literal, NDArrayFloat
from colour.utilities import closest, optional, validate_method

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "mesopic_weighting_function",
    "sd_mesopic_luminous_efficiency_function",
]


def mesopic_weighting_function(
    wavelength: ArrayLike,
    L_p: float,
    source: Literal["Blue Heavy", "Red Heavy"] | str = "Blue Heavy",
    method: Literal["MOVE", "LRC"] | str = "MOVE",
    photopic_lef: SpectralDistribution | None = None,
    scotopic_lef: SpectralDistribution | None = None,
) -> NDArrayFloat:
    """
    Calculate the mesopic weighting function factor :math:`V_m` at given
    wavelength :math:`\\lambda` using the photopic luminance :math:`L_p`.

    Parameters
    ----------
    wavelength
        Wavelength :math:`\\lambda` to calculate the mesopic weighting function
        factor.
    L_p
        Photopic luminance :math:`L_p`.
    source
        Light source colour temperature.
    method
        Method to calculate the weighting factor.
    photopic_lef
        :math:`V(\\lambda)` photopic luminous efficiency function, default to
        the *CIE 1924 Photopic Standard Observer*.
    scotopic_lef
        :math:`V^\\prime(\\lambda)` scotopic luminous efficiency function,
        default to the *CIE 1951 Scotopic Standard Observer*.

    Returns
    -------
    :class:`numpy.ndarray`
        Mesopic weighting function factor :math:`V_m`.

    References
    ----------
    :cite:`Wikipedia2005d`

    Examples
    --------
    >>> mesopic_weighting_function(500, 0.2)  # doctest: +ELLIPSIS
    0.7052200...
    """

    photopic_lef = optional(
        photopic_lef,
        SDS_LEFS_PHOTOPIC["CIE 1924 Photopic Standard Observer"],
    )

    scotopic_lef = optional(
        scotopic_lef,
        SDS_LEFS_SCOTOPIC["CIE 1951 Scotopic Standard Observer"],
    )

    source = validate_method(
        source,
        ("Blue Heavy", "Red Heavy"),
        '"{0}" light source colour temperature is invalid, '
        "it must be one of {1}!",
    )
    method = validate_method(method, ("MOVE", "LRC"))

    mesopic_x_luminance_values = sorted(DATA_MESOPIC_X.keys())
    index = mesopic_x_luminance_values.index(
        closest(mesopic_x_luminance_values, L_p)
    )
    x = DATA_MESOPIC_X[mesopic_x_luminance_values[index]][source][method]

    V_m = (1 - x) * scotopic_lef[wavelength] + x * photopic_lef[wavelength]

    return V_m


def sd_mesopic_luminous_efficiency_function(
    L_p: float,
    source: Literal["Blue Heavy", "Red Heavy"] | str = "Blue Heavy",
    method: Literal["MOVE", "LRC"] | str = "MOVE",
    photopic_lef: SpectralDistribution | None = None,
    scotopic_lef: SpectralDistribution | None = None,
) -> SpectralDistribution:
    """
    Return the mesopic luminous efficiency function :math:`V_m(\\lambda)` for
    given photopic luminance :math:`L_p`.

    Parameters
    ----------
    L_p
        Photopic luminance :math:`L_p`.
    source
        Light source colour temperature.
    method
        Method to calculate the weighting factor.
    photopic_lef
        :math:`V(\\lambda)` photopic luminous efficiency function, default to
        the *CIE 1924 Photopic Standard Observer*.
    scotopic_lef
        :math:`V^\\prime(\\lambda)` scotopic luminous efficiency function,
        default to the *CIE 1951 Scotopic Standard Observer*.

    Returns
    -------
    :class:`colour.SpectralDistribution`
        Mesopic luminous efficiency function :math:`V_m(\\lambda)`.

    References
    ----------
    :cite:`Wikipedia2005d`

    Examples
    --------
    >>> from colour.utilities import numpy_print_options
    >>> with numpy_print_options(suppress=True):
    ...     sd_mesopic_luminous_efficiency_function(0.2)  # doctest: +ELLIPSIS
    ...
    SpectralDistribution([[ 380.        ,    0.000424 ...],
                          [ 381.        ,    0.0004781...],
                          [ 382.        ,    0.0005399...],
                          [ 383.        ,    0.0006122...],
                          [ 384.        ,    0.0006961...],
                          [ 385.        ,    0.0007929...],
                          [ 386.        ,    0.000907 ...],
                          [ 387.        ,    0.0010389...],
                          [ 388.        ,    0.0011923...],
                          [ 389.        ,    0.0013703...],
                          [ 390.        ,    0.0015771...],
                          [ 391.        ,    0.0018167...],
                          [ 392.        ,    0.0020942...],
                          [ 393.        ,    0.0024160...],
                          [ 394.        ,    0.0027888...],
                          [ 395.        ,    0.0032196...],
                          [ 396.        ,    0.0037222...],
                          [ 397.        ,    0.0042957...],
                          [ 398.        ,    0.0049531...],
                          [ 399.        ,    0.0057143...],
                          [ 400.        ,    0.0065784...],
                          [ 401.        ,    0.0075658...],
                          [ 402.        ,    0.0086912...],
                          [ 403.        ,    0.0099638...],
                          [ 404.        ,    0.0114058...],
                          [ 405.        ,    0.0130401...],
                          [ 406.        ,    0.0148750...],
                          [ 407.        ,    0.0169310...],
                          [ 408.        ,    0.0192211...],
                          [ 409.        ,    0.0217511...],
                          [ 410.        ,    0.0245342...],
                          [ 411.        ,    0.0275773...],
                          [ 412.        ,    0.0309172...],
                          [ 413.        ,    0.0345149...],
                          [ 414.        ,    0.0383998...],
                          [ 415.        ,    0.0425744...],
                          [ 416.        ,    0.0471074...],
                          [ 417.        ,    0.0519322...],
                          [ 418.        ,    0.0570541...],
                          [ 419.        ,    0.0625466...],
                          [ 420.        ,    0.0683463...],
                          [ 421.        ,    0.0745255...],
                          [ 422.        ,    0.0809440...],
                          [ 423.        ,    0.0877344...],
                          [ 424.        ,    0.0948915...],
                          [ 425.        ,    0.1022731...],
                          [ 426.        ,    0.109877 ...],
                          [ 427.        ,    0.1178421...],
                          [ 428.        ,    0.1260316...],
                          [ 429.        ,    0.1343772...],
                          [ 430.        ,    0.143017 ...],
                          [ 431.        ,    0.1518128...],
                          [ 432.        ,    0.1608328...],
                          [ 433.        ,    0.1700088...],
                          [ 434.        ,    0.1792726...],
                          [ 435.        ,    0.1886934...],
                          [ 436.        ,    0.1982041...],
                          [ 437.        ,    0.2078032...],
                          [ 438.        ,    0.2174184...],
                          [ 439.        ,    0.2271147...],
                          [ 440.        ,    0.2368196...],
                          [ 441.        ,    0.2464623...],
                          [ 442.        ,    0.2561153...],
                          [ 443.        ,    0.2657160...],
                          [ 444.        ,    0.2753387...],
                          [ 445.        ,    0.2848520...],
                          [ 446.        ,    0.2944648...],
                          [ 447.        ,    0.3034902...],
                          [ 448.        ,    0.3132347...],
                          [ 449.        ,    0.3223257...],
                          [ 450.        ,    0.3314513...],
                          [ 451.        ,    0.3406129...],
                          [ 452.        ,    0.3498117...],
                          [ 453.        ,    0.3583617...],
                          [ 454.        ,    0.3676377...],
                          [ 455.        ,    0.3762670...],
                          [ 456.        ,    0.3849392...],
                          [ 457.        ,    0.3936540...],
                          [ 458.        ,    0.4024077...],
                          [ 459.        ,    0.4111965...],
                          [ 460.        ,    0.4193298...],
                          [ 461.        ,    0.4281803...],
                          [ 462.        ,    0.4363804...],
                          [ 463.        ,    0.4453117...],
                          [ 464.        ,    0.4542949...],
                          [ 465.        ,    0.4626509...],
                          [ 466.        ,    0.4717570...],
                          [ 467.        ,    0.4809300...],
                          [ 468.        ,    0.4901776...],
                          [ 469.        ,    0.4995075...],
                          [ 470.        ,    0.5096145...],
                          [ 471.        ,    0.5191293...],
                          [ 472.        ,    0.5294259...],
                          [ 473.        ,    0.5391316...],
                          [ 474.        ,    0.5496217...],
                          [ 475.        ,    0.5602103...],
                          [ 476.        ,    0.5702197...],
                          [ 477.        ,    0.5810207...],
                          [ 478.        ,    0.5919093...],
                          [ 479.        ,    0.6028683...],
                          [ 480.        ,    0.6138806...],
                          [ 481.        ,    0.6249373...],
                          [ 482.        ,    0.6360619...],
                          [ 483.        ,    0.6465989...],
                          [ 484.        ,    0.6579538...],
                          [ 485.        ,    0.6687841...],
                          [ 486.        ,    0.6797939...],
                          [ 487.        ,    0.6909887...],
                          [ 488.        ,    0.7023827...],
                          [ 489.        ,    0.7133032...],
                          [ 490.        ,    0.7244513...],
                          [ 491.        ,    0.7358470...],
                          [ 492.        ,    0.7468118...],
                          [ 493.        ,    0.7580294...],
                          [ 494.        ,    0.7694964...],
                          [ 495.        ,    0.7805225...],
                          [ 496.        ,    0.7917805...],
                          [ 497.        ,    0.8026123...],
                          [ 498.        ,    0.8130793...],
                          [ 499.        ,    0.8239297...],
                          [ 500.        ,    0.8352251...],
                          [ 501.        ,    0.8456342...],
                          [ 502.        ,    0.8564818...],
                          [ 503.        ,    0.8676921...],
                          [ 504.        ,    0.8785021...],
                          [ 505.        ,    0.8881489...],
                          [ 506.        ,    0.8986405...],
                          [ 507.        ,    0.9079322...],
                          [ 508.        ,    0.9174255...],
                          [ 509.        ,    0.9257739...],
                          [ 510.        ,    0.9350656...],
                          [ 511.        ,    0.9432365...],
                          [ 512.        ,    0.9509063...],
                          [ 513.        ,    0.9586931...],
                          [ 514.        ,    0.9658413...],
                          [ 515.        ,    0.9722825...],
                          [ 516.        ,    0.9779924...],
                          [ 517.        ,    0.9836106...],
                          [ 518.        ,    0.9883465...],
                          [ 519.        ,    0.9920964...],
                          [ 520.        ,    0.9954436...],
                          [ 521.        ,    0.9976202...],
                          [ 522.        ,    0.9993457...],
                          [ 523.        ,    1.       ...],
                          [ 524.        ,    0.9996498...],
                          [ 525.        ,    0.9990487...],
                          [ 526.        ,    0.9975356...],
                          [ 527.        ,    0.9957615...],
                          [ 528.        ,    0.9930143...],
                          [ 529.        ,    0.9899559...],
                          [ 530.        ,    0.9858741...],
                          [ 531.        ,    0.9814453...],
                          [ 532.        ,    0.9766885...],
                          [ 533.        ,    0.9709363...],
                          [ 534.        ,    0.9648947...],
                          [ 535.        ,    0.9585832...],
                          [ 536.        ,    0.952012 ...],
                          [ 537.        ,    0.9444916...],
                          [ 538.        ,    0.9367089...],
                          [ 539.        ,    0.9293506...],
                          [ 540.        ,    0.9210429...],
                          [ 541.        ,    0.9124772...],
                          [ 542.        ,    0.9036604...],
                          [ 543.        ,    0.8945958...],
                          [ 544.        ,    0.8845999...],
                          [ 545.        ,    0.8750500...],
                          [ 546.        ,    0.8659457...],
                          [ 547.        ,    0.8559224...],
                          [ 548.        ,    0.8456846...],
                          [ 549.        ,    0.8352499...],
                          [ 550.        ,    0.8253229...],
                          [ 551.        ,    0.8152079...],
                          [ 552.        ,    0.8042205...],
                          [ 553.        ,    0.7944209...],
                          [ 554.        ,    0.7837466...],
                          [ 555.        ,    0.7735680...],
                          [ 556.        ,    0.7627808...],
                          [ 557.        ,    0.7522710...],
                          [ 558.        ,    0.7417549...],
                          [ 559.        ,    0.7312909...],
                          [ 560.        ,    0.7207983...],
                          [ 561.        ,    0.7101939...],
                          [ 562.        ,    0.6996362...],
                          [ 563.        ,    0.6890656...],
                          [ 564.        ,    0.6785599...],
                          [ 565.        ,    0.6680593...],
                          [ 566.        ,    0.6575697...],
                          [ 567.        ,    0.6471578...],
                          [ 568.        ,    0.6368208...],
                          [ 569.        ,    0.6264871...],
                          [ 570.        ,    0.6161541...],
                          [ 571.        ,    0.6058896...],
                          [ 572.        ,    0.5957000...],
                          [ 573.        ,    0.5855937...],
                          [ 574.        ,    0.5754412...],
                          [ 575.        ,    0.5653883...],
                          [ 576.        ,    0.5553742...],
                          [ 577.        ,    0.5454680...],
                          [ 578.        ,    0.5355972...],
                          [ 579.        ,    0.5258267...],
                          [ 580.        ,    0.5160152...],
                          [ 581.        ,    0.5062322...],
                          [ 582.        ,    0.4965595...],
                          [ 583.        ,    0.4868746...],
                          [ 584.        ,    0.4773299...],
                          [ 585.        ,    0.4678028...],
                          [ 586.        ,    0.4583704...],
                          [ 587.        ,    0.4489722...],
                          [ 588.        ,    0.4397606...],
                          [ 589.        ,    0.4306131...],
                          [ 590.        ,    0.4215446...],
                          [ 591.        ,    0.4125681...],
                          [ 592.        ,    0.4037550...],
                          [ 593.        ,    0.3950359...],
                          [ 594.        ,    0.3864104...],
                          [ 595.        ,    0.3778777...],
                          [ 596.        ,    0.3694405...],
                          [ 597.        ,    0.3611074...],
                          [ 598.        ,    0.3528596...],
                          [ 599.        ,    0.3447056...],
                          [ 600.        ,    0.3366470...],
                          [ 601.        ,    0.3286917...],
                          [ 602.        ,    0.3208410...],
                          [ 603.        ,    0.3130808...],
                          [ 604.        ,    0.3054105...],
                          [ 605.        ,    0.2978225...],
                          [ 606.        ,    0.2903027...],
                          [ 607.        ,    0.2828727...],
                          [ 608.        ,    0.2755311...],
                          [ 609.        ,    0.2682900...],
                          [ 610.        ,    0.2611478...],
                          [ 611.        ,    0.2541176...],
                          [ 612.        ,    0.2471885...],
                          [ 613.        ,    0.2403570...],
                          [ 614.        ,    0.2336057...],
                          [ 615.        ,    0.2269379...],
                          [ 616.        ,    0.2203527...],
                          [ 617.        ,    0.2138465...],
                          [ 618.        ,    0.2073946...],
                          [ 619.        ,    0.2009789...],
                          [ 620.        ,    0.1945818...],
                          [ 621.        ,    0.1881943...],
                          [ 622.        ,    0.1818226...],
                          [ 623.        ,    0.1754987...],
                          [ 624.        ,    0.1692476...],
                          [ 625.        ,    0.1630876...],
                          [ 626.        ,    0.1570257...],
                          [ 627.        ,    0.151071 ...],
                          [ 628.        ,    0.1452469...],
                          [ 629.        ,    0.1395845...],
                          [ 630.        ,    0.1341087...],
                          [ 631.        ,    0.1288408...],
                          [ 632.        ,    0.1237666...],
                          [ 633.        ,    0.1188631...],
                          [ 634.        ,    0.1141075...],
                          [ 635.        ,    0.1094766...],
                          [ 636.        ,    0.1049613...],
                          [ 637.        ,    0.1005679...],
                          [ 638.        ,    0.0962924...],
                          [ 639.        ,    0.0921296...],
                          [ 640.        ,    0.0880778...],
                          [ 641.        ,    0.0841306...],
                          [ 642.        ,    0.0802887...],
                          [ 643.        ,    0.0765559...],
                          [ 644.        ,    0.0729367...],
                          [ 645.        ,    0.0694345...],
                          [ 646.        ,    0.0660491...],
                          [ 647.        ,    0.0627792...],
                          [ 648.        ,    0.0596278...],
                          [ 649.        ,    0.0565970...],
                          [ 650.        ,    0.0536896...],
                          [ 651.        ,    0.0509068...],
                          [ 652.        ,    0.0482444...],
                          [ 653.        ,    0.0456951...],
                          [ 654.        ,    0.0432510...],
                          [ 655.        ,    0.0409052...],
                          [ 656.        ,    0.0386537...],
                          [ 657.        ,    0.0364955...],
                          [ 658.        ,    0.0344285...],
                          [ 659.        ,    0.0324501...],
                          [ 660.        ,    0.0305579...],
                          [ 661.        ,    0.0287496...],
                          [ 662.        ,    0.0270233...],
                          [ 663.        ,    0.0253776...],
                          [ 664.        ,    0.0238113...],
                          [ 665.        ,    0.0223226...],
                          [ 666.        ,    0.0209086...],
                          [ 667.        ,    0.0195688...],
                          [ 668.        ,    0.0183056...],
                          [ 669.        ,    0.0171216...],
                          [ 670.        ,    0.0160192...],
                          [ 671.        ,    0.0149986...],
                          [ 672.        ,    0.0140537...],
                          [ 673.        ,    0.0131784...],
                          [ 674.        ,    0.0123662...],
                          [ 675.        ,    0.0116107...],
                          [ 676.        ,    0.0109098...],
                          [ 677.        ,    0.0102587...],
                          [ 678.        ,    0.0096476...],
                          [ 679.        ,    0.0090665...],
                          [ 680.        ,    0.0085053...],
                          [ 681.        ,    0.0079567...],
                          [ 682.        ,    0.0074229...],
                          [ 683.        ,    0.0069094...],
                          [ 684.        ,    0.0064213...],
                          [ 685.        ,    0.0059637...],
                          [ 686.        ,    0.0055377...],
                          [ 687.        ,    0.0051402...],
                          [ 688.        ,    0.00477  ...],
                          [ 689.        ,    0.0044263...],
                          [ 690.        ,    0.0041081...],
                          [ 691.        ,    0.0038149...],
                          [ 692.        ,    0.0035456...],
                          [ 693.        ,    0.0032984...],
                          [ 694.        ,    0.0030718...],
                          [ 695.        ,    0.0028639...],
                          [ 696.        ,    0.0026738...],
                          [ 697.        ,    0.0025000...],
                          [ 698.        ,    0.0023401...],
                          [ 699.        ,    0.0021918...],
                          [ 700.        ,    0.0020526...],
                          [ 701.        ,    0.0019207...],
                          [ 702.        ,    0.001796 ...],
                          [ 703.        ,    0.0016784...],
                          [ 704.        ,    0.0015683...],
                          [ 705.        ,    0.0014657...],
                          [ 706.        ,    0.0013702...],
                          [ 707.        ,    0.001281 ...],
                          [ 708.        ,    0.0011976...],
                          [ 709.        ,    0.0011195...],
                          [ 710.        ,    0.0010464...],
                          [ 711.        ,    0.0009776...],
                          [ 712.        ,    0.0009131...],
                          [ 713.        ,    0.0008525...],
                          [ 714.        ,    0.0007958...],
                          [ 715.        ,    0.0007427...],
                          [ 716.        ,    0.0006929...],
                          [ 717.        ,    0.0006462...],
                          [ 718.        ,    0.0006026...],
                          [ 719.        ,    0.0005619...],
                          [ 720.        ,    0.0005240...],
                          [ 721.        ,    0.0004888...],
                          [ 722.        ,    0.0004561...],
                          [ 723.        ,    0.0004255...],
                          [ 724.        ,    0.0003971...],
                          [ 725.        ,    0.0003704...],
                          [ 726.        ,    0.0003455...],
                          [ 727.        ,    0.0003221...],
                          [ 728.        ,    0.0003001...],
                          [ 729.        ,    0.0002796...],
                          [ 730.        ,    0.0002604...],
                          [ 731.        ,    0.0002423...],
                          [ 732.        ,    0.0002254...],
                          [ 733.        ,    0.0002095...],
                          [ 734.        ,    0.0001947...],
                          [ 735.        ,    0.0001809...],
                          [ 736.        ,    0.0001680...],
                          [ 737.        ,    0.0001560...],
                          [ 738.        ,    0.0001449...],
                          [ 739.        ,    0.0001345...],
                          [ 740.        ,    0.0001249...],
                          [ 741.        ,    0.0001159...],
                          [ 742.        ,    0.0001076...],
                          [ 743.        ,    0.0000999...],
                          [ 744.        ,    0.0000927...],
                          [ 745.        ,    0.0000862...],
                          [ 746.        ,    0.0000801...],
                          [ 747.        ,    0.0000745...],
                          [ 748.        ,    0.0000693...],
                          [ 749.        ,    0.0000646...],
                          [ 750.        ,    0.0000602...],
                          [ 751.        ,    0.0000561...],
                          [ 752.        ,    0.0000523...],
                          [ 753.        ,    0.0000488...],
                          [ 754.        ,    0.0000456...],
                          [ 755.        ,    0.0000425...],
                          [ 756.        ,    0.0000397...],
                          [ 757.        ,    0.0000370...],
                          [ 758.        ,    0.0000346...],
                          [ 759.        ,    0.0000322...],
                          [ 760.        ,    0.0000301...],
                          [ 761.        ,    0.0000281...],
                          [ 762.        ,    0.0000262...],
                          [ 763.        ,    0.0000244...],
                          [ 764.        ,    0.0000228...],
                          [ 765.        ,    0.0000213...],
                          [ 766.        ,    0.0000198...],
                          [ 767.        ,    0.0000185...],
                          [ 768.        ,    0.0000173...],
                          [ 769.        ,    0.0000161...],
                          [ 770.        ,    0.0000150...],
                          [ 771.        ,    0.0000140...],
                          [ 772.        ,    0.0000131...],
                          [ 773.        ,    0.0000122...],
                          [ 774.        ,    0.0000114...],
                          [ 775.        ,    0.0000106...],
                          [ 776.        ,    0.0000099...],
                          [ 777.        ,    0.0000092...],
                          [ 778.        ,    0.0000086...],
                          [ 779.        ,    0.0000080...],
                          [ 780.        ,    0.0000075...]],
                         SpragueInterpolator,
                         {},
                         Extrapolator,
                         {'method': 'Constant', 'left': None, 'right': None})
    """

    photopic_lef = optional(
        photopic_lef,
        SDS_LEFS_PHOTOPIC["CIE 1924 Photopic Standard Observer"],
    )

    scotopic_lef = optional(
        scotopic_lef,
        SDS_LEFS_SCOTOPIC["CIE 1951 Scotopic Standard Observer"],
    )

    shape = SpectralShape(
        max([photopic_lef.shape.start, scotopic_lef.shape.start]),
        min([photopic_lef.shape.end, scotopic_lef.shape.end]),
        max([photopic_lef.shape.interval, scotopic_lef.shape.interval]),
    )

    sd = SpectralDistribution(
        mesopic_weighting_function(
            shape.wavelengths, L_p, source, method, photopic_lef, scotopic_lef
        ),
        shape.wavelengths,
        name=f"{L_p} Lp Mesopic Luminous Efficiency Function",
    )

    return sd.normalise()
