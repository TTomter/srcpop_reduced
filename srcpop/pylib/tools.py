from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def set_theme(argv):
    plt.rcParams['figure.figsize']=[5,3]
    # sns.set_theme('notebook' if 'talk' not in argv else 'talk', font_scale=1.25) 
    sns.set_theme( 'talk', font_scale=1.) 
    if 'paper' in argv: 
        # sns.set_theme('paper')
        sns.set_style('ticks')
    if 'dark' in argv:
        sns.set_style('darkgrid') ##?
        plt.style.use('dark_background')
        plt.rcParams['grid.color']='0.5'
        # plt.rcParams['figure.facecolor']='k'
        dark_mode=True
    else:
        dark_mode=False
        sns.set_style('ticks' if 'paper' in argv else 'whitegrid')
        plt.rcParams['figure.facecolor']='white'
    return dark_mode

def fpeak_kw(axis='x'):
    return {axis+'label':r'Peak flux $F_p\ \ \mathrm{ (eV\ cm^{-2}\ s^{-1})}$', 
            axis+'ticks': np.arange(-2,4.9,2),
            axis+'ticklabels': '$10^{-2}$ 1 100 $10^4$'.split(),
            axis+'lim': (-2,5 ),
            }
def diffuse_kw(axis='x'):
    return {axis+'label':r'Diffuse energy flux $\mathrm{ (eV\ cm^{-2}\ s^{-1}\ deg^{-2})} $',
            axis+'lim': (-1,2.2),
            axis+'ticks': np.arange(-1,2.1,1),
            axis+'ticklabels': '0.1 1 10 100'.split(),
           }
def epeak_kw(axis='x', show_100=False):
    return {axis+'label':'$E_p$  (GeV)',
            axis+'ticks': np.arange(-1,1.1 if not show_100 else 2.1,1),
            axis+'ticklabels':('0.1 1 10 ' if not show_100 else '0.1 1 10 100').split(),
            }


def var_kw(axis='x'):
    return {axis+'label':'Variability index',
            axis+'ticks': np.arange(0,4.1,1),
            axis+'ticklabels':'1 10 100 $10^3$ $10^4$'.split(),
            }           

def ternary_plot(df, columns=None, ax=None):
    import ternary
    if columns is None: 
        columns=df.columns
    assert len(columns==3)
    fig, ax = plt.subplots(figsize=(8,8))

    tax = ternary.TernaryAxesSubplot(ax=ax,)
    
    tax.right_corner_label(columns[0], fontsize=16)
    tax.top_corner_label(columns[1], fontsize=16)
    tax.left_corner_label(columns[2], fontsize=16)
    tax.scatter(df.iloc[:,0:3].to_numpy(), marker='o',
                s=10,c=None, vmin=None, vmax=None)#'cyan');
    ax.grid(False); ax.axis('off')
    tax.clear_matplotlib_ticks()
    tax.set_background_color('0.3')
    tax.boundary()
    return fig


@dataclass
class FigNum:
    n : float = 0
    dn : float= 1
    @property
    def current(self): return self.n if self.dn==1 else f'{self.n:.1f}'
    @property
    def next(self):
        self.n += self.dn
        return self.current
    def __repr__(self):
        return self.current
    
def show_date():
    from pylib.ipynb_docgen import show
    import datetime
    date=str(datetime.datetime.now())[:16]
    show(f"""<h5 style="text-align:right; margin-right:15px"> {date}</h5>""")

def update_legend(ax, data, hue, **kwargs):
    """ seaborn companion to insert counts in legend,
    perhaps change location or fontsize
    """
    gs = data.groupby(hue).size()
    leg = ax.get_legend()
    fontsize = kwargs.pop('fontsize', None)
    leg.set(**kwargs)

    for tobj in leg.get_texts():
        text = tobj.get_text()
        if fontsize is not None: tobj.set(fontsize=fontsize)
        if text in gs.index:
            tobj.set_text(f'({gs[text]}) {text}', )


def curly(x,y, scale, ax=None, color='k'):
    import matplotlib.transforms as mtrans
    from matplotlib.text import TextPath
    from matplotlib.patches import PathPatch
    
    if not ax: ax=plt.gca()
    tp = TextPath((0, 0), "}", size=1)
    trans = mtrans.Affine2D().scale(1, scale) + \
        mtrans.Affine2D().translate(x,y) + ax.transData
    pp = PathPatch(tp, lw=0, fc=color, transform=trans)
    ax.add_artist(pp)

def curly_demo():
    X = [0,1,2,3,4]
    Y = [1,1,2,2,3]
    S = [1,2,3,4,1]
    fig, ax = plt.subplots()

    for x,y,s in zip(X,Y,S):
        curly(x,y,s, ax=ax)

    ax.axis([0,5,0,7])
    plt.show()


def set_glon(df):
    """ add a signed glon, `sglon` column range (180,-180) """

    glon = df.glon.values.copy()
    glon[glon>180]-=360
    df['sglon'] = glon

def galactic_axes(ax, lat=(-10,11, 2), lon=(180,-181, -30), **kwargs):
    """set axis ticks, labels for Galactic coordinates
    """
    xticks=np.arange(*lon)
    yticks=np.arange(*lat)
    def lmap(ticks):
        return list(map(lambda x: rf'${x}^\circ$',ticks))
    ax.set(
        xlim=lon[:2],  xticks=xticks, xlabel='$l$',
        xticklabels=lmap( np.where(xticks<0, xticks+360, xticks)),
        ylim=lat[:2],  yticks=yticks, ylabel='$b$',
        yticklabels=lmap(yticks),
        **kwargs)