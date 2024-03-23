/**
   Copyright (c) Dev Berry Group www.dev-berry.com
   @author Kassem Farhat 
**/

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __FONTS_H
#define __FONTS_H


/*鏈�澶у瓧浣撳井杞泤榛�24 (32x41) */
#define MAX_HEIGHT_FONT         41
#define MAX_WIDTH_FONT          32
#define OFFSET_BITMAP           

#ifdef __cplusplus
 extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include <stdint.h>
#include <avr/pgmspace.h>
//ASCII
typedef struct _tFont
{    
  const uint8_t *table;
  uint16_t Width;
  uint16_t Height;
  
} sFONT;


//GB2312
typedef struct                                          // 姹夊瓧瀛楁ā鏁版嵁缁撴瀯
{
  unsigned char index[3];                               // 姹夊瓧鍐呯爜绱㈠紩
  const char matrix[MAX_HEIGHT_FONT*MAX_WIDTH_FONT/8];  // 鐐归樀鐮佹暟鎹�
}CH_CN;


typedef struct
{    
  const CH_CN *table;
  uint16_t size;
  uint16_t ASCII_Width;
  uint16_t Width;
  uint16_t Height;
  
}cFONT;

extern sFONT Font24;
extern sFONT Font20;
extern sFONT Font16;
extern sFONT Font12;
extern sFONT Font8;

extern cFONT Font12CN;
extern cFONT Font24CN;
extern const unsigned char Font16_Table[];

#ifdef __cplusplus
}
#endif
  
#endif /* __FONTS_H */
 

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/

