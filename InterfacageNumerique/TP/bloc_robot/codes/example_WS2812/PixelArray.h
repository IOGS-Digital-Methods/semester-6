/**
 * FILENAME :        PixelArray.h          
 *
 * DESCRIPTION :
 *       Pixel Array class definition / Especially for LEDs Strips
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    25/oct/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */

#ifndef     __PIXEL_ARRAY_H_HEADER_H__
#define     __PIXEL_ARRAY_H_HEADER_H__

#define     WS2812_STD      24
#define     WS2812_WHI      32


class PixelArray{
    public:
        /**
        */
        PixelArray(int nb_pixels, int nb_bits);
        /**
        */
        void set_all_RGB(short r, short g, short b);
        /**
        */
        void set_pix_RGB(int pix, short r, short g, short b);
        /**
        */
        int* get_array(void);
        /**
        */
        void set_black_all();

    private:
        int *_array;
        int __nb_pixels;
        int __nb_bits;

};

#endif