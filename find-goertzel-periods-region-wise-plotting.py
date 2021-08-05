#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

We find periodicity at various frequencies

- Normalize to a unit variance to avoid the scale effect
- Add reactivity vector or read from a file
- outputs: csv and the corresponding plot


"""

__author__      = "Jitender"
__copyright__   = "CopyLeft"


import matplotlib as mpl
mpl.use('Agg')
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
sns.set()
# Bigger than normal fonts
sns.set(font_scale=0.45, rc={"lines.linewidth": 1.0})

from numpy import array, zeros, fft, cos, pi, arange, sqrt, exp, float64, mean, std

def avgCols(a):
    return 1.0*sum(a) / len(a)
    
def zscale(a, sigma = 1.0):
    mu = mean(a,None)
    sigma = std(a)
    return ( (array(a)-mu)/sigma)

def goertzel(x, period):
   ## ref: https://en.wikipedia.org/wiki/Goertzel_algorithm
   """
   Nterms defined here
   Kterm selected here
  
   power = sprev2 * sprev2 + sprev * sprev - coeff * sprev * sprev2
   """
   L=len(x)

   coeff=2.0*cos(2*pi/period)
   sprev, sprev2 =0.0,0.0
   for t in range(L):
     s= x[t] +  coeff * sprev - sprev2
     #sprev2, sprev =  sprev,  s   # using swap 
     sprev2=sprev
     sprev=s
   power = sqrt( (sprev*sprev) + (sprev2*sprev2)  - coeff*sprev*sprev2 )  
   return power

#==========================================================
def GetPowerPERD(vect):
  """
   Power specturm finding
  """
  sigo = zscale(vect)# 

  ### signal, period we get power
  pwr=[]
  period=[]
  for perd in range(2, len(sigo) + 1):
     gotty=goertzel(sigo, perd) 
     print( "pwr" + str(perd), "  ",  gotty)
     period.append(perd)
     pwr.append(gotty)

  print '-'*80
  max_pwr, max_period = sorted( zip(pwr, period))[-1]
  print( "max_PWR, max_PER: ",  max_pwr, max_period)
  return  sigo, period, pwr, max_pwr, max_period

#=== data region ======================================
def getPortion(viv, title=''):
    while True:
       head=viv.readline().strip()
       rect=viv.readline().strip().split('\t')
       if not head or len(head) < 1:
          break
       yield head, map(float,rect)
          

####
def PlotterBLOCK(vectH, prefo, titos):
      with sns.axes_style("darkgrid"):
         ax =plt.subplot(211)
         x = np.arange(1,len(vectH)+1)
         #plt.plot(x, vectH, 'r',   label='High')
         #plt.plot(x, vectM, 'g--', label='Medium')
         #plt.plot(x, vectL, 'b:',  label='Low')
         plt.plot(x, vectH, 'r',        label=titos)

         if True:
           # Now add the legend with some customizations.
           legend = ax.legend(loc='upper right', shadow=False)
           #legend = ax.legend(loc='best', shadow=True)

           # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
           frame = legend.get_frame()
           frame.set_facecolor('0.45')

           # Set the fontsize
           for label in legend.get_texts():
               label.set_fontsize('small')
           for label in legend.get_lines():
               label.set_linewidth(0.25)  # the legend line width    
         #------------------------------------------------------------------------
         sigoH, periodH, pwrH, max_pwrH, max_periodH = GetPowerPERD(vectH)

         with open(prefo + "-period-data.csv",'w') as out:
            out.write('Period' + ',' + 'Magnitude' + '\n')
            for h, m  in zip(periodH, pwrH):
                out.write(str(h) + ',' + str(m) + '\n')

         axH = plt.subplot(212)
         axH.plot(periodH, pwrH, color='orange')

         plt.xlabel('Period')
         plt.ylabel('Magnitude')

         axH.annotate(r'$3$',
                   xy=(periodH[1], pwrH[1]), xycoords='data',
                   xytext=(10, 20), textcoords='offset points', fontsize=8,
                   arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

         plt.savefig(prefo + "-panel.png", dpi=600)
         plt.close("all") 


if __name__ == '__main__':

        # extracted values
        medD =  {'5UTR': ['0.230040533', '0.228661575', '0.234222611', '0.230040533', '0.22982429', '0.230613483', '0.231980204', '0.23587608', '0.23402957', '0.23402957', '0.228551646', '0.231980204', '0.22982429', '0.234334702', '0.236020059', '0.233673627', '0.230613483', '0.230613483', '0.233673627', '0.228661575', '0.230613483', '0.227538891', '0.230967944', '0.23587608', '0.231980204', '0.231117186', '0.225040179', '0.232648995', '0.226440316', '0.224408453', '0.232648995', '0.23587608', '0.232590375', '0.229424473', '0.23587608', '0.228184326', '0.227333101', '0.230967944', '0.230675792', '0.230613483', '0.239586945', '0.230040533', '0.232648995', '0.231980204', '0.233673627', '0.225561994', '0.236933818', '0.234054799', '0.232590375', '0.233404313', '0.232590375', '0.226892141', '0.229424473', '0.229424473', '0.234841599', '0.223987641', '0.228184326', '0.233693292', '0.231117186', '0.229917857', '0.232648995', '0.235716106', '0.226802365', '0.232634305', '0.232648995', '0.230967944', '0.233095585', '0.238211338', '0.230967944', '0.232634305', '0.231594092', '0.234054799', '0.232918423', '0.233095585', '0.234980716', '0.22878917', '0.229949321', '0.228551646', '0.235330008', '0.239586945', '0.236933818', '0.234524181', '0.227937767', '0.234346033', '0.232590375', '0.23587608', '0.232948368', '0.23362925', '0.235776372', '0.235977655', '0.23587608', '0.233404313', '0.242718638', '0.23750453', '0.237512138', '0.234346033', '0.242005261', '0.234445755', '0.234445755', '0.23587608', '0.23586431', '0.238795062', '0.239586945', '0.236020059', '0.236486982', '0.236933818', '0.237199204', '0.235600802', '0.239913581', '0.240671254', '0.246383026', '0.23989589', '0.242345923', '0.241958625', '0.235266731', '0.239343338', '0.239945651', '0.240410199', '0.251035558', '0.254056464', '0.24746519', '0.258815534', '0.24686153', '0.247545093', '0.25643411', '0.246637162', '0.252046812', '0.250772329', '0.264767131', '0.254272631', '0.25289418', '0.25650227', '0.248748146', '0.257985082', '0.257163443', '0.264332068', '0.267557646', '0.272069531', '0.271275001', '0.271275001', '0.268540875', '0.267476556', '0.274474966', '0.270325474', '0.268899825', '0.269080826', '0.270401644', '0.276743753', '0.267499373', '0.27162464', '0.270239585', '0.272402143', '0.278128904', '0.284453185', '0.272217271', '0.277700712', '0.273712711', '0.283919785', '0.277226119', '0.276743753', '0.285464881', '0.284026892', '0.280929556', '0.27966746', '0.292757862', '0.280398853', '0.273210349', '0.28418626', '0.279174769', '0.289252099', '0.284460444', '0.282018982', '0.290927936', '0.289639991', '0.281402717', '0.296061111', '0.290927936', '0.293993759', '0.282350238', '0.292950905', '0.290144063', '0.291362117', '0.311985669', '0.307481666', '0.305696381', '0.304286471', '0.30211819', '0.315588343', '0.328079539', '0.298285987', '0.318852989', '0.293809701', '0.313870458', '0.339047268', '0.349661015', '0.338593435', '0.349234738', '0.399611234', '0.424800294', '0.279895855', '0.311319344'], '3CDS': ['0.309702983', '0.306205256', '0.310254737', '0.319373318', '0.293050038', '0.308674722', '0.312961578', '0.314800638', '0.310330431', '0.29903562', '0.323457763', '0.305430531', '0.315475084', '0.325276071', '0.311366238', '0.316962137', '0.318823795', '0.295654545', '0.312729675', '0.306547737', '0.305910814', '0.30838767', '0.317371207', '0.307808899', '0.29855756', '0.307917014', '0.313217343', '0.323173167', '0.301950896', '0.298415246', '0.303605243', '0.312167518', '0.324565799', '0.31220379', '0.305386876', '0.300983953', '0.311246454', '0.318784326', '0.309697111', '0.314415459', '0.297659597', '0.295347214', '0.31877715', '0.310338855', '0.303123245', '0.299873784', '0.315265758', '0.312775061', '0.302719567', '0.311523829', '0.311587978', '0.305810532', '0.306186355', '0.311824136', '0.293908202', '0.308458015', '0.301566642', '0.315723094', '0.313805084', '0.305910814', '0.313869661', '0.315801207', '0.304593318', '0.315363444', '0.303036255', '0.29604135', '0.300290939', '0.314049675', '0.308506094', '0.309892274', '0.302966665', '0.305914019', '0.302501289', '0.321062087', '0.296229976', '0.312004378', '0.31886746', '0.318881682', '0.308726279', '0.299891875', '0.31761248', '0.302057515', '0.303752634', '0.311448304', '0.319855411', '0.316153809', '0.30456334', '0.307038733', '0.299700045', '0.304048813', '0.309404465', '0.296006704', '0.297628762', '0.289578758', '0.291457356', '0.290178387', '0.312909761', '0.293733108', '0.298393703', '0.297608519', '0.302703438', '0.303937559', '0.311539652', '0.318720859', '0.317449678', '0.312801499', '0.310966431', '0.312252106', '0.309989713', '0.305906219', '0.29193201', '0.297002466', '0.313649365', '0.288644417', '0.293925467', '0.310996207', '0.300350692', '0.307291343', '0.296158265', '0.302427552', '0.306819308', '0.307438102', '0.292781425', '0.310291341', '0.303822082', '0.313012885', '0.311591734', '0.304382332', '0.296046017', '0.305717762', '0.306497066', '0.311264429', '0.289972188', '0.307572387', '0.297432225', '0.307020529', '0.307268829', '0.316162364', '0.306169706', '0.298493115', '0.3070986', '0.31395967', '0.306297564', '0.304683796', '0.305534292', '0.310876601', '0.283919785', '0.29310924', '0.31422637', '0.306628708', '0.289106904', '0.293662107', '0.293152378', '0.281345937', '0.287124191', '0.292820474', '0.290716179', '0.290984884', '0.297236305', '0.295407711', '0.292820474', '0.286769831', '0.297959255', '0.287963079', '0.293908202', '0.284028347', '0.288914146', '0.277313905', '0.280898147', '0.279895855', '0.285462474', '0.273728521', '0.272687288', '0.285679143', '0.280242101', '0.276507754', '0.290185081', '0.279476414', '0.277167303', '0.273712711', '0.276697794', '0.286058023', '0.261903617', '0.26917591', '0.280855555', '0.275315044', '0.264563443', '0.278789877', '0.275600057', '0.256949596', '0.278832406', '0.262042218', '0.259262863', '0.249924679', '0.28081609', '0.268701199', '0.261953109', '0.341913377', '0.39072484', '0.336005614', '0.296284526'], '3UTR': ['0.273210349', '0.271995497', '0.267144978', '0.265117281', '0.276229593', '0.275600057', '0.270442939', '0.272217271', '0.280221419', '0.267458329', '0.267552191', '0.271029716', '0.269814578', '0.267229511', '0.265638164', '0.259655722', '0.271629987', '0.264085401', '0.263489518', '0.262913993', '0.265727805', '0.257225363', '0.261643901', '0.267470084', '0.265891387', '0.268050662', '0.2664763', '0.259489628', '0.266853916', '0.26500234', '0.259936967', '0.264575655', '0.257668546', '0.258387625', '0.259409304', '0.265414818', '0.258586795', '0.261067135', '0.260320546', '0.256924902', '0.25888343', '0.255559826', '0.263103598', '0.255268762', '0.25446758', '0.257871539', '0.256226768', '0.255268762', '0.255471443', '0.252426737', '0.259636447', '0.25446758', '0.260677343', '0.252169477', '0.257758209', '0.251468065', '0.258387625', '0.264236187', '0.256924902', '0.261067135', '0.260823727', '0.258870215', '0.252405827', '0.252405827', '0.25888343', '0.254735087', '0.259754486', '0.252804358', '0.252405827', '0.249542464', '0.258238985', '0.254182464', '0.251362484', '0.251687631', '0.254112231', '0.255135624', '0.248442335', '0.251060921', '0.258548343', '0.249924679', '0.25329729', '0.253550416', '0.254272631', '0.251362484', '0.255360211', '0.247979475', '0.24872189', '0.24355186', '0.249726475', '0.24665997', '0.251687631', '0.243798765', '0.249202309', '0.248219579', '0.249870965', '0.245974419', '0.252426737', '0.24033074', '0.242979795', '0.246341312', '0.24623574', '0.245067222', '0.240106795', '0.24247646', '0.239721669', '0.242498837', '0.241937411', '0.240410199', '0.246046829', '0.239778291', '0.24623574', '0.236550381', '0.240671254', '0.238535672', '0.246046829', '0.237512138', '0.238854959', '0.23587608', '0.237602505', '0.237146014', '0.234334702', '0.241117291', '0.237212628', '0.232852467', '0.234265057', '0.234735852', '0.234265057', '0.233165213', '0.23362925', '0.238211338', '0.236706044', '0.236300041', '0.237790261', '0.233599087', '0.23402957', '0.23362925', '0.232634305', '0.234883788', '0.232545359', '0.231315577', '0.229300427', '0.230179718', '0.231618777', '0.229811303', '0.230892545', '0.232047444', '0.230277279', '0.234735852', '0.228184326', '0.232047444', '0.229388312', '0.226802365', '0.233137806', '0.22982429', '0.229300427', '0.22982429', '0.229418992', '0.231315577', '0.2244566', '0.226401143', '0.227504885', '0.230277279', '0.228158946', '0.229949321', '0.226237369', '0.22784303', '0.226212503', '0.226440316', '0.225923347', '0.221205049', '0.221354257', '0.224680233', '0.225432842', '0.221354257', '0.217410604', '0.225432842', '0.223543644', '0.221512925', '0.220609267', '0.224680233', '0.219252065', '0.223777666', '0.219252065', '0.219340469', '0.221169835', '0.21951829', '0.224694284', '0.222063332', '0.220094548', '0.220866016', '0.223609685', '0.219440544', '0.221169835', '0.220869187', '0.220909674', '0.221433993', '0.22146476', '0.219440544', '0.225432842', '0.21908314', '0.221205049'], '5CDS': ['0.305534344', '0.320511671', '0.269188128', '0.257855995', '0.268596342', '0.283113874', '0.275941814', '0.296585691', '0.303553407', '0.291487683', '0.307578498', '0.309746995', '0.286008911', '0.308270761', '0.309126616', '0.298081872', '0.301551853', '0.308086193', '0.291969647', '0.294332747', '0.29832408', '0.289737589', '0.291795808', '0.303578776', '0.299206646', '0.289296543', '0.298335972', '0.293754697', '0.28807537', '0.289106904', '0.283829062', '0.292820474', '0.288674948', '0.292820474', '0.285957536', '0.291486013', '0.299675369', '0.285030032', '0.301193369', '0.295463371', '0.294021257', '0.303475854', '0.307909083', '0.286105443', '0.303847407', '0.30138236', '0.300813912', '0.303269957', '0.300707248', '0.296455309', '0.312787739', '0.313716055', '0.309395474', '0.308927888', '0.317313779', '0.316113786', '0.311218309', '0.298546584', '0.297132116', '0.319108468', '0.319777969', '0.306452549', '0.316165625', '0.308238342', '0.314534419', '0.331446981', '0.300010356', '0.303463352', '0.301621648', '0.31017773', '0.298685638', '0.296812332', '0.303648574', '0.31608579', '0.314002996', '0.302992435', '0.306366716', '0.325551896', '0.303028581', '0.322030997', '0.308715102', '0.313057253', '0.318182532', '0.317605776', '0.301659236', '0.301467089', '0.322156515', '0.313206875', '0.316774134', '0.30996806', '0.300024759', '0.312760487', '0.322789495', '0.310090429', '0.315769866', '0.302795425', '0.296284526', '0.292483351', '0.307384399', '0.29452891', '0.303335422', '0.312945678', '0.303798486', '0.28705704', '0.31633499', '0.30795012', '0.306487081', '0.340281923', '0.312563651', '0.310088967', '0.327762175', '0.338769861', '0.331647362', '0.331108781', '0.293906396', '0.311350124', '0.322346828', '0.304821879', '0.31466464', '0.331369346', '0.301659236', '0.317820032', '0.305813622', '0.31053862', '0.314675792', '0.324033936', '0.316583196', '0.318920076', '0.296284526', '0.304048813', '0.323090845', '0.316076468', '0.290988003', '0.322992659', '0.3170611', '0.309525946', '0.312167699', '0.327086308', '0.297893123', '0.315801207', '0.310498198', '0.300908352', '0.311308902', '0.328417148', '0.301550785', '0.314372766', '0.331262037', '0.320440951', '0.312061368', '0.328470921', '0.322032299', '0.312005124', '0.317335392', '0.326645286', '0.322191839', '0.322294504', '0.3182031', '0.316263854', '0.313256546', '0.306907756', '0.306056154', '0.345683623', '0.318543485', '0.301948867', '0.308968919', '0.303243615', '0.321432264', '0.305895769', '0.313503123', '0.292970294', '0.316737536', '0.318159461', '0.311394505', '0.312595905', '0.31403207', '0.314195831', '0.319993113', '0.323621023', '0.312363437', '0.323575795', '0.318648775', '0.30116347', '0.313224745', '0.310972005', '0.313699418', '0.322785429', '0.314503487', '0.312012932', '0.31849059', '0.303642715', '0.301931786', '0.324157382', '0.29881026', '0.298585316', '0.326770327', '0.314757841', '0.318975374', '0.327482284', '0.30739953', '0.307555919', '0.305146476']}

        # the desired selection  
        head = medD['5CDS'][12:]  
        tail = medD['3CDS'][:-90] 

        # made the input vector
        med_rect = head +  tail

        reg_title, rect = 'trimmed3CDS', med_rect   #  region title and the vector

        reactivity_vector = [ float(x) for x in rect]

        PlotterBLOCK(reactivity_vector, reg_title, reg_title) 

        print ('Done')



