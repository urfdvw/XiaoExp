- READ;
- vol;voltage:
- reg_R;Ref R:
    - r_1k;1K
    - r_10k;10K
    - r_1m;1M
    - r_10m;10M
- sen_R;Sensor R:
- phy; 
- Settings
    - scr_ori;screen orientation
        - scr_fix;fixed
        - scr_up;sense up
        - scr_do;sense down
    - screen brightness
        - bri_fix;fixed
        - bri_pos;pos. related
        - bri_inv;inv. related
    - Alarm
        - alm_re;reading:
        - alm_thr;thr=
        - alm_if;if:
            - alm_F;False
            - alm_lt;reading<thr
            - alm_gt;reading>thr
        - then:alarm on
        - alm_else;else:
            - alm_nth;nothing
            - alm_stp;alarm off
    - Temperature
        - temp_disp;toggle display
        - temp_clb0;calibrate 0c
        - temp_clb100;calibrate 100c
    - Average
        - alpha;Num of samples:
        - read_raw;RAW:
        - read_flt;averaged:
- Extra
    - vol_gra;voltage graph