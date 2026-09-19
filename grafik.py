import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data yang Anda berikan untuk state 
state_data = [
        {"action": [
                480,
                170
            ],
            "q_value": -4.7108
        },
        {
            "action": [
                540,
                130
            ],
            "q_value": -17.4657
        },
        {
            "action": [
                510,
                180
            ],
            "q_value": -4.4391
        },
        {
            "action": [
                490,
                220
            ],
            "q_value": -5.962
        },
        {
            "action": [
                560,
                170
            ],
            "q_value": -9.411
        },
        {
            "action": [
                550,
                190
            ],
            "q_value": -4.7284
        },
        {
            "action": [
                440,
                240
            ],
            "q_value": -14.5294
        },
        {
            "action": [
                490,
                210
            ],
            "q_value": -4.17
        },
        {
            "action": [
                610,
                50
            ],
            "q_value": -40.2621
        },
        {
            "action": [
                460,
                230
            ],
            "q_value": -10.6667
        },
        {
            "action": [
                400,
                250
            ],
            "q_value": -20.9077
        },
        {
            "action": [
                540,
                140
            ],
            "q_value": -15.0912
        },
        {
            "action": [
                540,
                210
            ],
            "q_value": -0.168
        },
        {
            "action": [
                400,
                320
            ],
            "q_value": -31.6889
        },
        {
            "action": [
                590,
                80
            ],
            "q_value": -31.7866
        },
        {
            "action": [
                460,
                190
            ],
            "q_value": -3.1938
        },
        {
            "action": [
                440,
                260
            ],
            "q_value": -17.8771
        },
        {
            "action": [
                520,
                230
            ],
            "q_value": -4.9493
        },
        {
            "action": [
                640,
                50
            ],
            "q_value": -40.5942
        },
        {
            "action": [
                700,
                50
            ],
            "q_value": -41.1067
        },
        {
            "action": [
                550,
                110
            ],
            "q_value": -22.8167
        },
        {
            "action": [
                420,
                290
            ],
            "q_value": -24.8817
        },
        {
            "action": [
                490,
                260
            ],
            "q_value": -12.6253
        },
        {
            "action": [
                400,
                260
            ],
            "q_value": -22.597
        },
        {
            "action": [
                420,
                280
            ],
            "q_value": -23.36
        },
        {
            "action": [
                640,
                100
            ],
            "q_value": -28.0676
        },
        {
            "action": [
                400,
                270
            ],
            "q_value": -24.2328
        },
        {
            "action": [
                590,
                130
            ],
            "q_value": -19.5514
        },
        {
            "action": [
                400,
                280
            ],
            "q_value": -25.8176
        },
        {
            "action": [
                570,
                180
            ],
            "q_value": -7.844
        },
        {
            "action": [
                430,
                320
            ],
            "q_value": -27.9773
        },
        {
            "action": [
                410,
                310
            ],
            "q_value": -29.0236
        },
        {
            "action": [
                420,
                260
            ],
            "q_value": -20.1735
        },
        {
            "action": [
                690,
                50
            ],
            "q_value": -41.0338
        },
        {
            "action": [
                420,
                290
            ],
            "q_value": -47.2752
        },
        {
            "action": [
                630,
                60
            ],
            "q_value": -37.813
        },
        {
            "action": [
                450,
                270
            ],
            "q_value": -18.3625
        },
        {
            "action": [
                470,
                240
            ],
            "q_value": -11.3676
        },
        {
            "action": [
                640,
                80
            ],
            "q_value": -32.8778
        },
        {
            "action": [
                560,
                90
            ],
            "q_value": -28.3292
        },
        {
            "action": [
                510,
                230
            ],
            "q_value": -5.8446
        },
        {
            "action": [
                520,
                210
            ],
            "q_value": -1.5041
        },
        {
            "action": [
                400,
                290
            ],
            "q_value": -27.3536
        },
        {
            "action": [
                700,
                50
            ],
            "q_value": -78.1027
        },
        {
            "action": [
                610,
                100
            ],
            "q_value": -27.2718
        },
        {
            "action": [
                430,
                290
            ],
            "q_value": -23.6931
        },
        {
            "action": [
                590,
                110
            ],
            "q_value": -24.2443
        },
        {
            "action": [
                400,
                300
            ],
            "q_value": -28.8429
        },
        {
            "action": [
                560,
                170
            ],
            "q_value": -17.8808
        },
        {
            "action": [
                480,
                220
            ],
            "q_value": -6.9114
        },
        {
            "action": [
                590,
                140
            ],
            "q_value": -17.2973
        },
        {
            "action": [
                560,
                160
            ],
            "q_value": -11.5556
        },
        {
            "action": [
                510,
                150
            ],
            "q_value": -11.1864
        },
        {
            "action": [
                540,
                190
            ],
            "q_value": -4.1534
        },
        {
            "action": [
                640,
                60
            ],
            "q_value": -37.9514
        },
        {
            "action": [
                450,
                250
            ],
            "q_value": -15.1357
        },
        {
            "action": [
                510,
                210
            ],
            "q_value": -2.3708
        },
        {
            "action": [
                630,
                60
            ],
            "q_value": -71.8448
        },
        {
            "action": [
                440,
                270
            ],
            "q_value": -19.4761
        },
        {
            "action": [
                580,
                150
            ],
            "q_value": -14.6685
        },
        {
            "action": [
                400,
                310
            ],
            "q_value": -30.2873
        },
        {
            "action": [
                570,
                80
            ],
            "q_value": -31.2815
        },
        {
            "action": [
                440,
                310
            ],
            "q_value": -25.4187
        },
        {
            "action": [
                430,
                240
            ],
            "q_value": -15.6403
        },
        {
            "action": [
                510,
                210
            ],
            "q_value": -4.5046
        },
        {
            "action": [
                450,
                230
            ],
            "q_value": -11.7074
        },
        {
            "action": [
                400,
                270
            ],
            "q_value": -46.0424
        },
        {
            "action": [
                550,
                180
            ],
            "q_value": -6.7822
        },
        {
            "action": [
                670,
                60
            ],
            "q_value": -38.3274
        },
        {
            "action": [
                510,
                220
            ],
            "q_value": -4.1329
        },
        {
            "action": [
                630,
                50
            ],
            "q_value": -40.4897
        },
        {
            "action": [
                530,
                220
            ],
            "q_value": -2.3907
        },
        {
            "action": [
                630,
                70
            ],
            "q_value": -35.21
        },
        {
            "action": [
                520,
                180
            ],
            "q_value": -5.0543
        },
        {
            "action": [
                480,
                220
            ],
            "q_value": -13.1317
        },
        {
            "action": [
                570,
                150
            ],
            "q_value": -14.2208
        },
        {
            "action": [
                560,
                150
            ],
            "q_value": -13.7577
        },
        {
            "action": [
                470,
                260
            ],
            "q_value": -14.6479
        },
        {
            "action": [
                650,
                90
            ],
            "q_value": -30.6608
        },
        {
            "action": [
                520,
                210
            ],
            "q_value": -2.8578
        },
        {
            "action": [
                580,
                160
            ],
            "q_value": -12.5081
        },
        {
            "action": [
                450,
                240
            ],
            "q_value": -13.4478
        },
        {
            "action": [
                610,
                110
            ],
            "q_value": -24.8819
        },
        {
            "action": [
                400,
                330
            ],
            "q_value": -33.0493
        },
        {
            "action": [
                690,
                60
            ],
            "q_value": -38.548
        },
        {
            "action": [
                420,
                310
            ],
            "q_value": -27.7918
        },
        {
            "action": [
                400,
                340
            ],
            "q_value": -34.3703
        },
        {
            "action": [
                400,
                350
            ],
            "q_value": -35.6533
        },
        {
            "action": [
                450,
                250
            ],
            "q_value": -28.7579
        },
        {
            "action": [
                570,
                110
            ],
            "q_value": -23.5574
        },
        {
            "action": [
                520,
                150
            ],
            "q_value": -11.7373
        },
        {
            "action": [
                670,
                50
            ],
            "q_value": -40.8736
        },
        {
            "action": [
                540,
                150
            ],
            "q_value": -12.7826
        },
        {
            "action": [
                480,
                240
            ],
            "q_value": -10.3667
        },
        {
            "action": [
                480,
                170
            ],
            "q_value": -8.9505
        },
        {
            "action": [
                550,
                130
            ],
            "q_value": -17.9132
        },
        {
            "action": [
                600,
                130
            ],
            "q_value": -19.926
        },
        {
            "action": [
                470,
                240
            ],
            "q_value": -21.5985
        },
        {
            "action": [
                530,
                150
            ],
            "q_value": -12.2691
        },
        {
            "action": [
                540,
                210
            ],
            "q_value": -0.3192
        },
        {
            "action": [
                630,
                60
            ],
            "q_value": -102.4733
        },
        {
            "action": [
                410,
                240
            ],
            "q_value": -17.9554
        },
        {
            "action": [
                610,
                70
            ],
            "q_value": -34.8456
        },
        {
            "action": [
                410,
                250
            ],
            "q_value": -19.6894
        },
        {
            "action": [
                410,
                260
            ],
            "q_value": -21.3687
        },
        {
            "action": [
                530,
                150
            ],
            "q_value": -23.3113
        },
        {
            "action": [
                420,
                280
            ],
            "q_value": -44.384
        },
        {
            "action": [
                440,
                260
            ],
            "q_value": -33.9666
        },
        {
            "action": [
                410,
                270
            ],
            "q_value": -22.9956
        },
        {
            "action": [
                410,
                280
            ],
            "q_value": -24.5725
        },
        {
            "action": [
                620,
                90
            ],
            "q_value": -29.9746
        },
        {
            "action": [
                650,
                60
            ],
            "q_value": -38.0831
        },
        {
            "action": [
                410,
                290
            ],
            "q_value": -26.1014
        },
        {
            "action": [
                620,
                90
            ],
            "q_value": -56.9518
        },
        {
            "action": [
                410,
                300
            ],
            "q_value": -27.5845
        },
        {
            "action": [
                610,
                100
            ],
            "q_value": -51.8165
        },
        {
            "action": [
                550,
                100
            ],
            "q_value": -25.3769
        },
        {
            "action": [
                410,
                320
            ],
            "q_value": -30.4205
        },
        {
            "action": [
                620,
                130
            ],
            "q_value": -20.6373
        },
        {
            "action": [
                410,
                330
            ],
            "q_value": -31.777
        },
        {
            "action": [
                410,
                340
            ],
            "q_value": -33.0947
        },
        {
            "action": [
                420,
                230
            ],
            "q_value": -15.0031
        },
        {
            "action": [
                610,
                90
            ],
            "q_value": -29.7271
        },
        {
            "action": [
                420,
                240
            ],
            "q_value": -16.7818
        },
        {
            "action": [
                460,
                210
            ],
            "q_value": -7.0478
        },
        {
            "action": [
                420,
                250
            ],
            "q_value": -18.5045
        },
        {
            "action": [
                400,
                250
            ],
            "q_value": -39.7246
        },
        {
            "action": [
                420,
                330
            ],
            "q_value": -30.536
        },
        {
            "action": [
                420,
                270
            ],
            "q_value": -21.7913
        },
        {
            "action": [
                420,
                300
            ],
            "q_value": -26.3583
        },
        {
            "action": [
                670,
                70
            ],
            "q_value": -35.8473
        },
        {
            "action": [
                400,
                260
            ],
            "q_value": -42.9342
        },
        {
            "action": [
                540,
                150
            ],
            "q_value": -24.287
        },
        {
            "action": [
                430,
                310
            ],
            "q_value": -26.5905
        },
        {
            "action": [
                690,
                50
            ],
            "q_value": -77.9642
        },
        {
            "action": [
                420,
                320
            ],
            "q_value": -29.1838
        },
        {
            "action": [
                540,
                180
            ],
            "q_value": -6.225
        },
        {
            "action": [
                640,
                60
            ],
            "q_value": -72.1077
        },
        {
            "action": [
                620,
                90
            ],
            "q_value": -81.2313
        },
        {
            "action": [
                430,
                220
            ],
            "q_value": -12.0508
        },
        {
            "action": [
                430,
                230
            ],
            "q_value": -13.8742
        },
        {
            "action": [
                590,
                160
            ],
            "q_value": -12.9613
        },
        {
            "action": [
                440,
                280
            ],
            "q_value": -21.0278
        },
        {
            "action": [
                400,
                260
            ],
            "q_value": -61.2378
        },
        {
            "action": [
                520,
                130
            ],
            "q_value": -16.52
        },
        {
            "action": [
                430,
                250
            ],
            "q_value": -17.3515
        },
        {
            "action": [
                460,
                210
            ],
            "q_value": -13.3907
        },
        {
            "action": [
                680,
                60
            ],
            "q_value": -38.4405
        },
        {
            "action": [
                410,
                290
            ],
            "q_value": -49.5927
        },
        {
            "action": [
                420,
                330
            ],
            "q_value": -58.0184
        },
        {
            "action": [
                500,
                200
            ],
            "q_value": -1.4286
        },
        {
            "action": [
                600,
                120
            ],
            "q_value": -22.2167
        },
        {
            "action": [
                410,
                280
            ],
            "q_value": -46.6877
        },
        {
            "action": [
                570,
                170
            ],
            "q_value": -9.9149
        },
        {
            "action": [
                530,
                190
            ],
            "q_value": -3.5597
        },
        {
            "action": [
                430,
                260
            ],
            "q_value": -19.0101
        },
        {
            "action": [
                430,
                270
            ],
            "q_value": -20.6186
        },
        {
            "action": [
                430,
                280
            ],
            "q_value": -22.1789
        },
        {
            "action": [
                480,
                210
            ],
            "q_value": -5.1043
        },
        {
            "action": [
                470,
                200
            ],
            "q_value": -4.1836
        },
        {
            "action": [
                640,
                90
            ],
            "q_value": -30.4411
        },
        {
            "action": [
                430,
                300
            ],
            "q_value": -25.163
        },
        {
            "action": [
                470,
                190
            ],
            "q_value": -2.2439
        },
        {
            "action": [
                440,
                210
            ],
            "q_value": -9.0985
        },
        {
            "action": [
                440,
                220
            ],
            "q_value": -10.9667
        },
        {
            "action": [
                460,
                240
            ],
            "q_value": -12.3943
        },
        {
            "action": [
                630,
                70
            ],
            "q_value": -66.899
        },
        {
            "action": [
                440,
                230
            ],
            "q_value": -12.7761
        },
        {
            "action": [
                440,
                250
            ],
            "q_value": -16.229
        },
        {
            "action": [
                480,
                170
            ],
            "q_value": -12.7662
        },
        {
            "action": [
                580,
                140
            ],
            "q_value": -16.8861
        },
        {
            "action": [
                440,
                290
            ],
            "q_value": -22.5342
        },
        {
            "action": [
                580,
                140
            ],
            "q_value": -32.0836
        },
        {
            "action": [
                440,
                300
            ],
            "q_value": -23.9973
        },
        {
            "action": [
                450,
                200
            ],
            "q_value": -6.1462
        },
        {
            "action": [
                440,
                290
            ],
            "q_value": -42.8151
        },
        {
            "action": [
                450,
                210
            ],
            "q_value": -8.0591
        },
        {
            "action": [
                400,
                250
            ],
            "q_value": -56.6598
        },
        {
            "action": [
                450,
                220
            ],
            "q_value": -9.9119
        },
        {
            "action": [
                450,
                260
            ],
            "q_value": -16.7732
        },
        {
            "action": [
                450,
                280
            ],
            "q_value": -19.9055
        },
        {
            "action": [
                450,
                290
            ],
            "q_value": -21.4041
        },
        {
            "action": [
                510,
                220
            ],
            "q_value": -7.8525
        },
        {
            "action": [
                450,
                300
            ],
            "q_value": -22.86
        },
        {
            "action": [
                510,
                200
            ],
            "q_value": -0.5563
        },
        {
            "action": [
                430,
                230
            ],
            "q_value": -26.3611
        },
        {
            "action": [
                600,
                110
            ],
            "q_value": -24.569
        },
        {
            "action": [
                460,
                200
            ],
            "q_value": -5.1515
        },
        {
            "action": [
                460,
                220
            ],
            "q_value": -8.8853
        },
        {
            "action": [
                490,
                260
            ],
            "q_value": -23.9881
        },
        {
            "action": [
                460,
                250
            ],
            "q_value": -14.0704
        },
        {
            "action": [
                420,
                240
            ],
            "q_value": -31.8855
        },
        {
            "action": [
                400,
                330
            ],
            "q_value": -62.7937
        },
        {
            "action": [
                430,
                240
            ],
            "q_value": -29.7166
        },
        {
            "action": [
                590,
                160
            ],
            "q_value": -24.6265
        },
        {
            "action": [
                460,
                260
            ],
            "q_value": -15.6972
        },
        {
            "action": [
                460,
                270
            ],
            "q_value": -17.2767
        },
        {
            "action": [
                640,
                90
            ],
            "q_value": -57.8381
        },
        {
            "action": [
                470,
                190
            ],
            "q_value": -4.2635
        },
        {
            "action": [
                460,
                280
            ],
            "q_value": -18.8108
        },
        {
            "action": [
                460,
                290
            ],
            "q_value": -20.3013
        },
        {
            "action": [
                430,
                250
            ],
            "q_value": -32.9678
        },
        {
            "action": [
                470,
                180
            ],
            "q_value": -1.7585
        },
        {
            "action": [
                660,
                70
            ],
            "q_value": -35.6986
        },
        {
            "action": [
                470,
                210
            ],
            "q_value": -6.0632
        },
        {
            "action": [
                630,
                90
            ],
            "q_value": -30.2125
        },
        {
            "action": [
                510,
                150
            ],
            "q_value": -21.2541
        },
        {
            "action": [
                470,
                220
            ],
            "q_value": -7.8855
        },
        {
            "action": [
                470,
                230
            ],
            "q_value": -9.6529
        },
        {
            "action": [
                480,
                260
            ],
            "q_value": -13.6243
        },
        {
            "action": [
                470,
                250
            ],
            "q_value": -13.0319
        },
        {
            "action": [
                400,
                250
            ],
            "q_value": -71.9016
        },
        {
            "action": [
                470,
                270
            ],
            "q_value": -16.2176
        },
        {
            "action": [
                470,
                280
            ],
            "q_value": -17.7427
        },
        {
            "action": [
                510,
                240
            ],
            "q_value": -7.508
        },
        {
            "action": [
                480,
                180
            ],
            "q_value": -2.4636
        },
        {
            "action": [
                480,
                190
            ],
            "q_value": -1.3194
        },
        {
            "action": [
                480,
                200
            ],
            "q_value": -3.2412
        },
        {
            "action": [
                410,
                280
            ],
            "q_value": -66.5914
        },
        {
            "action": [
                480,
                230
            ],
            "q_value": -8.6648
        },
        {
            "action": [
                520,
                130
            ],
            "q_value": -31.388
        },
        {
            "action": [
                470,
                210
            ],
            "q_value": -11.5201
        },
        {
            "action": [
                640,
                110
            ],
            "q_value": -25.7547
        },
        {
            "action": [
                480,
                250
            ],
            "q_value": -12.0192
        },
        {
            "action": [
                440,
                210
            ],
            "q_value": -17.2871
        },
        {
            "action": [
                480,
                270
            ],
            "q_value": -15.184
        },
        {
            "action": [
                650,
                90
            ],
            "q_value": -58.2555
        },
        {
            "action": [
                400,
                270
            ],
            "q_value": -65.671
        },
        {
            "action": [
                490,
                160
            ],
            "q_value": -7.6631
        },
        {
            "action": [
                490,
                170
            ],
            "q_value": -5.3712
        },
        {
            "action": [
                490,
                180
            ],
            "q_value": -3.1448
        },
        {
            "action": [
                620,
                130
            ],
            "q_value": -39.2109
        },
        {
            "action": [
                490,
                190
            ],
            "q_value": -0.9809
        },
        {
            "action": [
                490,
                200
            ],
            "q_value": -2.3232
        },
        {
            "action": [
                450,
                240
            ],
            "q_value": -25.5509
        },
        {
            "action": [
                490,
                230
            ],
            "q_value": -7.7014
        },
        {
            "action": [
                530,
                160
            ],
            "q_value": -10.0014
        },
        {
            "action": [
                520,
                160
            ],
            "q_value": -9.4471
        },
        {
            "action": [
                490,
                240
            ],
            "q_value": -9.3904
        },
        {
            "action": [
                530,
                190
            ],
            "q_value": -6.7635
        },
        {
            "action": [
                490,
                250
            ],
            "q_value": -11.0311
        },
        {
            "action": [
                540,
                190
            ],
            "q_value": -7.8915
        },
        {
            "action": [
                500,
                150
            ],
            "q_value": -10.6154
        },
        {
            "action": [
                500,
                160
            ],
            "q_value": -8.2788
        },
        {
            "action": [
                430,
                270
            ],
            "q_value": -39.1753
        },
        {
            "action": [
                500,
                170
            ],
            "q_value": -6.009
        },
        {
            "action": [
                500,
                180
            ],
            "q_value": -3.8029
        },
        {
            "action": [
                550,
                180
            ],
            "q_value": -12.8862
        },
        {
            "action": [
                500,
                190
            ],
            "q_value": -1.658
        },
        {
            "action": [
                500,
                210
            ],
            "q_value": -3.2592
        },
        {
            "action": [
                500,
                220
            ],
            "q_value": -5.0361
        },
        {
            "action": [
                410,
                300
            ],
            "q_value": -52.4106
        },
        {
            "action": [
                450,
                270
            ],
            "q_value": -34.8888
        },
        {
            "action": [
                500,
                230
            ],
            "q_value": -6.7616
        },
        {
            "action": [
                500,
                240
            ],
            "q_value": -8.4378
        },
        {
            "action": [
                520,
                140
            ],
            "q_value": -14.0939
        },
        {
            "action": [
                550,
                160
            ],
            "q_value": -11.0549
        },
        {
            "action": [
                650,
                90
            ],
            "q_value": -83.0908
        },
        {
            "action": [
                590,
                120
            ],
            "q_value": -21.8662
        },
        {
            "action": [
                500,
                250
            ],
            "q_value": -10.0667
        },
        {
            "action": [
                480,
                190
            ],
            "q_value": -2.5069
        },
        {
            "action": [
                510,
                140
            ],
            "q_value": -13.5677
        },
        {
            "action": [
                510,
                160
            ],
            "q_value": -8.8731
        },
        {
            "action": [
                500,
                170
            ],
            "q_value": -11.417
        },
        {
            "action": [
                420,
                270
            ],
            "q_value": -41.4035
        },
        {
            "action": [
                490,
                210
            ],
            "q_value": -7.923
        },
        {
            "action": [
                510,
                170
            ],
            "q_value": -6.625
        },
        {
            "action": [
                510,
                190
            ],
            "q_value": -2.3129
        },
        {
            "action": [
                420,
                260
            ],
            "q_value": -38.3297
        },
        {
            "action": [
                520,
                170
            ],
            "q_value": -7.2203
        },
        {
            "action": [
                520,
                190
            ],
            "q_value": -2.9465
        },
        {
            "action": [
                520,
                200
            ],
            "q_value": -0.8944
        },
        {
            "action": [
                510,
                150
            ],
            "q_value": -30.315
        },
        {
            "action": [
                520,
                220
            ],
            "q_value": -3.2514
        },
        {
            "action": [
                530,
                120
            ],
            "q_value": -19.4723
        },
        {
            "action": [
                460,
                220
            ],
            "q_value": -16.8821
        },
        {
            "action": [
                530,
                130
            ],
            "q_value": -17.0015
        },
        {
            "action": [
                530,
                140
            ],
            "q_value": -14.6015
        },
        {
            "action": [
                640,
                60
            ],
            "q_value": -102.8484
        },
        {
            "action": [
                400,
                340
            ],
            "q_value": -65.3035
        },
        {
            "action": [
                530,
                170
            ],
            "q_value": -7.7957
        },
        {
            "action": [
                530,
                180
            ],
            "q_value": -5.6493
        },
        {
            "action": [
                530,
                200
            ],
            "q_value": -1.5247
        },
        {
            "action": [
                530,
                210
            ],
            "q_value": -0.6581
        },
        {
            "action": [
                430,
                280
            ],
            "q_value": -42.1399
        },
        {
            "action": [
                650,
                90
            ],
            "q_value": -105.4425
        },
        {
            "action": [
                650,
                90
            ],
            "q_value": -125.5591
        },
        {
            "action": [
                540,
                110
            ],
            "q_value": -22.4246
        },
        {
            "action": [
                530,
                200
            ],
            "q_value": -2.8968
        },
        {
            "action": [
                540,
                120
            ],
            "q_value": -19.9091
        },
        {
            "action": [
                520,
                180
            ],
            "q_value": -9.6031
        },
        {
            "action": [
                540,
                160
            ],
            "q_value": -10.5371
        },
        {
            "action": [
                540,
                170
            ],
            "q_value": -8.3521
        },
        {
            "action": [
                630,
                70
            ],
            "q_value": -95.4191
        },
        {
            "action": [
                520,
                140
            ],
            "q_value": -26.7785
        },
        {
            "action": [
                540,
                200
            ],
            "q_value": -2.1351
        },
        {
            "action": [
                550,
                120
            ],
            "q_value": -20.3299
        },
        {
            "action": [
                550,
                140
            ],
            "q_value": -15.5638
        },
        {
            "action": [
                500,
                210
            ],
            "q_value": -6.1924
        },
        {
            "action": [
                550,
                150
            ],
            "q_value": -13.2786
        },
        {
            "action": [
                550,
                170
            ],
            "q_value": -8.8903
        },
        {
            "action": [
                470,
                280
            ],
            "q_value": -33.7111
        },
        {
            "action": [
                510,
                230
            ],
            "q_value": -11.1047
        },
        {
            "action": [
                550,
                200
            ],
            "q_value": -2.7267
        },
        {
            "action": [
                500,
                180
            ],
            "q_value": -7.2256
        },
        {
            "action": [
                560,
                100
            ],
            "q_value": -25.7242
        },
        {
            "action": [
                560,
                110
            ],
            "q_value": -23.194
        },
        {
            "action": [
                430,
                240
            ],
            "q_value": -42.3852
        },
        {
            "action": [
                560,
                120
            ],
            "q_value": -20.7353
        },
        {
            "action": [
                560,
                130
            ],
            "q_value": -18.3449
        },
        {
            "action": [
                560,
                140
            ],
            "q_value": -16.02
        },
        {
            "action": [
                680,
                50
            ],
            "q_value": -40.9562
        },
        {
            "action": [
                500,
                180
            ],
            "q_value": -10.306
        },
        {
            "action": [
                560,
                180
            ],
            "q_value": -7.3216
        },
        {
            "action": [
                560,
                190
            ],
            "q_value": -5.2853
        },
        {
            "action": [
                570,
                90
            ],
            "q_value": -28.6318
        },
        {
            "action": [
                570,
                100
            ],
            "q_value": -26.0582
        },
        {
            "action": [
                570,
                120
            ],
            "q_value": -21.1261
        }
]



df_state = pd.DataFrame(state_data)
# Ubah nama kolom 'q' menjadi 'q_value' agar konsisten
df_state.rename(columns={'q': 'q_value'}, inplace=True)
df_state[['Action_Vol_Air', 'Action_Vol_Nutrisi']] = pd.DataFrame(df_state['action'].tolist(), index=df_state.index)

# --- Proses Pengurutan Data ---
# Urutkan data berdasarkan nilai Q, dari terendah (paling buruk) ke tertinggi (paling baik)
df_state_sorted = df_state.sort_values(by='q_value', ascending=True).reset_index()

# Cari indeks dan nilai dari aksi terbaik (yang sekarang ada di baris terakhir)
best_q_row = df_state_sorted.iloc[-1]
best_q_index = best_q_row.name
best_q_value = best_q_row['q_value']
best_action = best_q_row['action']

# --- Membuat Plot ---
plt.figure(figsize=(18, 10))

# Plot utama (garis)
plt.plot(df_state_sorted.index, df_state_sorted['q_value'], marker='.', linestyle='-', color='c', label='Perkembangan Nilai Q')

# Tandai titik terbaik dengan bintang merah
plt.plot(best_q_index, best_q_value, 
         marker='.', 
         markersize=10, 
         color='red', 
         linestyle='', # Tanpa garis
         label=f'Q Terbaik: {best_q_value:.2f}')

# Tambahkan anotasi untuk titik terbaik
plt.annotate(
    f'Aksi Terbaik: {best_action}',
    xy=(best_q_index, best_q_value),
    xytext=(best_q_index - 30, best_q_value - 15), # Penyesuaian posisi teks
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.7)
)

# Label dan Judul
plt.title('Simulasi Perkembangan Nilai Q untuk State (61, 1980)', fontsize=18)
plt.xlabel('Iterasi (Urutan Percobaan Aksi)', fontsize=14)
plt.ylabel('Nilai Q (Kualitas Aksi)', fontsize=14)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend(loc='upper left', fontsize=12)

# Menambahkan sentuhan akhir agar lebih jelas
plt.axhline(0, color='grey', linewidth=0.8, linestyle='--')
plt.fill_between(df_state_sorted.index, df_state_sorted['q_value'], -165, color='cyan', alpha=0.1)

plt.show()