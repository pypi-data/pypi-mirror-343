/**
 * @file   dwm.h
 * @author Zhu Dengda (zhudengda@mail.iggcas.ac.cn)
 * @date   2024-07-24
 * 
 * 以下代码实现的是 使用离散波数法求积分，参考：
 * 
 *         1. 姚振兴, 谢小碧. 2022/03. 理论地震图及其应用（初稿）.  
 *         2. Yao Z. X. and D. G. Harkrider. 1983. A generalized refelection-transmission coefficient 
 *               matrix and discrete wavenumber method for synthetic seismograms. BSSA. 73(6). 1685-1699
 * 
 */

#pragma once 

#include <stdio.h>

#include "common/model.h"
#include "common/kernel.h"


/**
 * 传统的离散波数积分，结果以三维数组的形式返回，形状为[nr][3][4], 分别代表震中距、阶数(m=0,1,2)
 * 和4种积分类型(p=0,1,2,3)
 * 
 * @param  mod1d     (in)`MODEL1D` 结构体指针
 * @param  dk        (in)波数积分间隔
 * @param  kmax      (in)波数积分的上限
 * @param  keps      (in)波数积分的收敛条件，要求在某震中距下所有格林函数都收敛，为负数代表不提前判断收敛，按照波数积分上限进行积分
 * @param  omega     (in)复数频率
 * @param  nr        (in)震中距数量
 * @param  rs        (in)震中距数组
 * 
 * @param  sum_EXP_J[nr][3][4]  (out)爆炸源
 * @param  sum_VF_J[nr][3][4]   (out)垂直力源
 * @param  sum_HF_J[nr][3][4]   (out)水平力源
 * @param  sum_DC_J[nr][3][4]   (out)剪切源
 * 
 * @param  calc_upar       (in)是否计算位移u的空间导数
 * @param  sum_EXP_uiz_J[nr][3][4]  (out)爆炸源产生的ui_z(位移u对坐标z的偏导)，下同
 * @param  sum_VF_uiz_J[nr][3][4]   (out)垂直力源
 * @param  sum_HF_uiz_J[nr][3][4]   (out)水平力源
 * @param  sum_DC_uiz_J[nr][3][4]   (out)剪切源
 * @param  sum_EXP_uir_J[nr][3][4]  (out)爆炸源产生的ui_r(位移u对坐标r的偏导)，下同
 * @param  sum_VF_uir_J[nr][3][4]   (out)垂直力源
 * @param  sum_HF_uir_J[nr][3][4]   (out)水平力源
 * @param  sum_DC_uir_J[nr][3][4]   (out)剪切源
 * 
 * @param  fstats               (out)文件指针，保存不同k值的格林函数积分核函数
 * @param  kerfunc              (in)计算核函数的函数指针
 * 
 * @return  k        积分截至时的波数
 */
MYREAL discrete_integ(
    const MODEL1D *mod1d, MYREAL dk, MYREAL kmax, MYREAL keps, MYCOMPLEX omega, 
    MYINT nr, MYREAL *rs,
    MYCOMPLEX sum_EXP_J[nr][3][4], MYCOMPLEX sum_VF_J[nr][3][4],  
    MYCOMPLEX sum_HF_J[nr][3][4],  MYCOMPLEX sum_DC_J[nr][3][4],  
    bool calc_upar,
    MYCOMPLEX sum_EXP_uiz_J[nr][3][4], MYCOMPLEX sum_VF_uiz_J[nr][3][4],  
    MYCOMPLEX sum_HF_uiz_J[nr][3][4],  MYCOMPLEX sum_DC_uiz_J[nr][3][4],  
    MYCOMPLEX sum_EXP_uir_J[nr][3][4], MYCOMPLEX sum_VF_uir_J[nr][3][4],  
    MYCOMPLEX sum_HF_uir_J[nr][3][4],  MYCOMPLEX sum_DC_uir_J[nr][3][4],  
    FILE *fstats, KernelFunc kerfunc);
