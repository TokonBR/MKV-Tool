import json, os, shutil, subprocess, threading, queue, hashlib, sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

BG='#080808'; PANEL='#151515'; FG='#f3f4f7'; MUTED='#a9afbf'; ACC='#454545'
CONFIG_PATH=Path(os.environ.get('APPDATA',str(Path.home()))) / 'MKV Tool' / 'settings.json'
KINDS={'video':'Vídeo','audio':'Áudio','subtitles':'Legenda'}
LANGUAGE_NAMES = {'aa': 'Afar', 'ab': 'Abkhazian', 'ae': 'Avestan', 'af': 'Afrikaans', 'ak': 'Akan', 'am': 'Amharic', 'an': 'Aragonese', 'ar': 'Arabic', 'as': 'Assamese', 'av': 'Avaric', 'ay': 'Aymara', 'az': 'Azerbaijani', 'ba': 'Bashkir', 'be': 'Belarusian', 'bg': 'Bulgarian', 'bi': 'Bislama', 'bm': 'Bambara', 'bn': 'Bengali', 'bo': 'Tibetan', 'br': 'Breton', 'bs': 'Bosnian', 'ca': 'Catalan', 'ce': 'Chechen', 'ch': 'Chamorro', 'co': 'Corsican', 'cr': 'Cree', 'cs': 'Czech', 'cu': 'Church Slavic', 'cv': 'Chuvash', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German', 'dv': 'Dhivehi', 'dz': 'Dzongkha', 'ee': 'Ewe', 'el': 'Modern Greek (1453-)', 'en': 'English', 'eo': 'Esperanto', 'es': 'Spanish', 'et': 'Estonian', 'eu': 'Basque', 'fa': 'Persian', 'ff': 'Fulah', 'fi': 'Finnish', 'fj': 'Fijian', 'fo': 'Faroese', 'fr': 'French', 'fy': 'Western Frisian', 'ga': 'Irish', 'gd': 'Scottish Gaelic', 'gl': 'Galician', 'gn': 'Guarani', 'gu': 'Gujarati', 'gv': 'Manx', 'ha': 'Hausa', 'he': 'Hebrew', 'hi': 'Hindi', 'ho': 'Hiri Motu', 'hr': 'Croatian', 'ht': 'Haitian', 'hu': 'Hungarian', 'hy': 'Armenian', 'hz': 'Herero', 'ia': 'Interlingua (International Auxiliary Language Association)', 'id': 'Indonesian', 'ie': 'Interlingue', 'ig': 'Igbo', 'ii': 'Sichuan Yi', 'ik': 'Inupiaq', 'io': 'Ido', 'is': 'Icelandic', 'it': 'Italian', 'iu': 'Inuktitut', 'ja': 'Japanese', 'jv': 'Javanese', 'ka': 'Georgian', 'kg': 'Kongo', 'ki': 'Kikuyu', 'kj': 'Kuanyama', 'kk': 'Kazakh', 'kl': 'Kalaallisut', 'km': 'Khmer', 'kn': 'Kannada', 'ko': 'Korean', 'kr': 'Kanuri', 'ks': 'Kashmiri', 'ku': 'Kurdish', 'kv': 'Komi', 'kw': 'Cornish', 'ky': 'Kirghiz', 'la': 'Latin', 'lb': 'Luxembourgish', 'lg': 'Ganda', 'li': 'Limburgan', 'ln': 'Lingala', 'lo': 'Lao', 'lt': 'Lithuanian', 'lu': 'Luba-Katanga', 'lv': 'Latvian', 'mg': 'Malagasy', 'mh': 'Marshallese', 'mi': 'Maori', 'mk': 'Macedonian', 'ml': 'Malayalam', 'mn': 'Mongolian', 'mr': 'Marathi', 'ms': 'Malay (macrolanguage)', 'mt': 'Maltese', 'my': 'Burmese', 'na': 'Nauru', 'nb': 'Norwegian Bokmål', 'nd': 'North Ndebele', 'ne': 'Nepali (macrolanguage)', 'ng': 'Ndonga', 'nl': 'Dutch', 'nn': 'Norwegian Nynorsk', 'no': 'Norwegian', 'nr': 'South Ndebele', 'nv': 'Navajo', 'ny': 'Nyanja', 'oc': 'Occitan (post 1500)', 'oj': 'Ojibwa', 'om': 'Oromo', 'or': 'Oriya (macrolanguage)', 'os': 'Ossetian', 'pa': 'Panjabi', 'pi': 'Pali', 'pl': 'Polish', 'ps': 'Pushto', 'pt': 'Portuguese', 'qu': 'Quechua', 'rm': 'Romansh', 'rn': 'Rundi', 'ro': 'Romanian', 'ru': 'Russian', 'rw': 'Kinyarwanda', 'sa': 'Sanskrit', 'sc': 'Sardinian', 'sd': 'Sindhi', 'se': 'Northern Sami', 'sg': 'Sango', 'sh': 'Serbo-Croatian', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian', 'sm': 'Samoan', 'sn': 'Shona', 'so': 'Somali', 'sq': 'Albanian', 'sr': 'Serbian', 'ss': 'Swati', 'st': 'Southern Sotho', 'su': 'Sundanese', 'sv': 'Swedish', 'sw': 'Swahili (macrolanguage)', 'ta': 'Tamil', 'te': 'Telugu', 'tg': 'Tajik', 'th': 'Thai', 'ti': 'Tigrinya', 'tk': 'Turkmen', 'tl': 'Tagalog', 'tn': 'Tswana', 'to': 'Tonga (Tonga Islands)', 'tr': 'Turkish', 'ts': 'Tsonga', 'tt': 'Tatar', 'tw': 'Twi', 'ty': 'Tahitian', 'ug': 'Uighur', 'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek', 've': 'Venda', 'vi': 'Vietnamese', 'vo': 'Volapük', 'wa': 'Walloon', 'wo': 'Wolof', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'za': 'Zhuang', 'zh': 'Chinese', 'zu': 'Zulu'}
LANGUAGE_ALIASES = {'aar': 'aa', 'abk': 'ab', 'afr': 'af', 'aka': 'ak', 'amh': 'am', 'ara': 'ar', 'arg': 'an', 'asm': 'as', 'ava': 'av', 'ave': 'ae', 'aym': 'ay', 'aze': 'az', 'bak': 'ba', 'bam': 'bm', 'bel': 'be', 'ben': 'bn', 'bis': 'bi', 'bod': 'bo', 'tib': 'bo', 'bos': 'bs', 'bre': 'br', 'bul': 'bg', 'cat': 'ca', 'ces': 'cs', 'cze': 'cs', 'cha': 'ch', 'che': 'ce', 'chu': 'cu', 'chv': 'cv', 'cor': 'kw', 'cos': 'co', 'cre': 'cr', 'cym': 'cy', 'wel': 'cy', 'dan': 'da', 'deu': 'de', 'ger': 'de', 'div': 'dv', 'dzo': 'dz', 'ell': 'el', 'gre': 'el', 'eng': 'en', 'epo': 'eo', 'est': 'et', 'eus': 'eu', 'baq': 'eu', 'ewe': 'ee', 'fao': 'fo', 'fas': 'fa', 'per': 'fa', 'fij': 'fj', 'fin': 'fi', 'fra': 'fr', 'fre': 'fr', 'fry': 'fy', 'ful': 'ff', 'gla': 'gd', 'gle': 'ga', 'glg': 'gl', 'glv': 'gv', 'grn': 'gn', 'guj': 'gu', 'hat': 'ht', 'hau': 'ha', 'hbs': 'sh', 'heb': 'he', 'her': 'hz', 'hin': 'hi', 'hmo': 'ho', 'hrv': 'hr', 'hun': 'hu', 'hye': 'hy', 'arm': 'hy', 'ibo': 'ig', 'ido': 'io', 'iii': 'ii', 'iku': 'iu', 'ile': 'ie', 'ina': 'ia', 'ind': 'id', 'ipk': 'ik', 'isl': 'is', 'ice': 'is', 'ita': 'it', 'jav': 'jv', 'jpn': 'ja', 'kal': 'kl', 'kan': 'kn', 'kas': 'ks', 'kat': 'ka', 'geo': 'ka', 'kau': 'kr', 'kaz': 'kk', 'khm': 'km', 'kik': 'ki', 'kin': 'rw', 'kir': 'ky', 'kom': 'kv', 'kon': 'kg', 'kor': 'ko', 'kua': 'kj', 'kur': 'ku', 'lao': 'lo', 'lat': 'la', 'lav': 'lv', 'lim': 'li', 'lin': 'ln', 'lit': 'lt', 'ltz': 'lb', 'lub': 'lu', 'lug': 'lg', 'mah': 'mh', 'mal': 'ml', 'mar': 'mr', 'mkd': 'mk', 'mac': 'mk', 'mlg': 'mg', 'mlt': 'mt', 'mon': 'mn', 'mri': 'mi', 'mao': 'mi', 'msa': 'ms', 'may': 'ms', 'mya': 'my', 'bur': 'my', 'nau': 'na', 'nav': 'nv', 'nbl': 'nr', 'nde': 'nd', 'ndo': 'ng', 'nep': 'ne', 'nld': 'nl', 'dut': 'nl', 'nno': 'nn', 'nob': 'nb', 'nor': 'no', 'nya': 'ny', 'oci': 'oc', 'oji': 'oj', 'ori': 'or', 'orm': 'om', 'oss': 'os', 'pan': 'pa', 'pli': 'pi', 'pol': 'pl', 'por': 'pt', 'pus': 'ps', 'que': 'qu', 'roh': 'rm', 'ron': 'ro', 'rum': 'ro', 'run': 'rn', 'rus': 'ru', 'sag': 'sg', 'san': 'sa', 'sin': 'si', 'slk': 'sk', 'slo': 'sk', 'slv': 'sl', 'sme': 'se', 'smo': 'sm', 'sna': 'sn', 'snd': 'sd', 'som': 'so', 'sot': 'st', 'spa': 'es', 'sqi': 'sq', 'alb': 'sq', 'srd': 'sc', 'srp': 'sr', 'ssw': 'ss', 'sun': 'su', 'swa': 'sw', 'swe': 'sv', 'tah': 'ty', 'tam': 'ta', 'tat': 'tt', 'tel': 'te', 'tgk': 'tg', 'tgl': 'tl', 'tha': 'th', 'tir': 'ti', 'ton': 'to', 'tsn': 'tn', 'tso': 'ts', 'tuk': 'tk', 'tur': 'tr', 'twi': 'tw', 'uig': 'ug', 'ukr': 'uk', 'urd': 'ur', 'uzb': 'uz', 'ven': 've', 'vie': 'vi', 'vol': 'vo', 'wln': 'wa', 'wol': 'wo', 'xho': 'xh', 'yid': 'yi', 'yor': 'yo', 'zha': 'za', 'zho': 'zh', 'chi': 'zh', 'zul': 'zu', 'fil': 'tl'}
def display_language(code):
    # Somente exibição: não altera metadados nem as opções de edição.
    return 'en' if str(code or '').strip().lower().replace('_','-') in ('en-us','eng') else code

def general_language(code):
    # Filtro em ISO 639-1; preserva a identificação original da faixa.
    value=str(code or 'und').strip().replace('_','-').lower()
    base=value.split('-',1)[0]
    return LANGUAGE_ALIASES.get(base,base)


def binary(name):
    p=shutil.which(name)
    if p:return p
    for root in [r'C:\Program Files\MKVToolNix',r'C:\Program Files (x86)\MKVToolNix']:
        f=os.path.join(root,name+'.exe')
        if os.path.isfile(f):return f
    return None

def inspect(path,exe):
    r=subprocess.run([exe,'-J',str(path)],capture_output=True,text=True,encoding='utf-8',errors='replace',creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    if r.returncode:raise RuntimeError(r.stderr.strip() or 'Erro ao analisar MKV')
    return json.loads(r.stdout)['tracks']

def signature(tracks):
    # Codec, idioma, ordem e sinalizadores definem o layout, não nomes pessoais das faixas.
    return tuple((t.get('type'),t.get('codec'),t.get('properties',{}).get('language_ietf') or t.get('properties',{}).get('language','und'),t.get('properties',{}).get('forced_track',False),t.get('properties',{}).get('default_track',False)) for t in tracks)

class App:
    def __init__(self,root):
        self.root=root;root.title('MKV Tool v1.0.0 by Tokon');root.geometry('1150x740');root.configure(bg=BG)
        self.settings=self.load_settings();self.settings.pop('track_choices',None);self.saved_output=self.settings.get('output_folder','');legacy=self.settings.get('visible_languages',['por','pt','pt-BR','en']);self.audio_langs={general_language(x) for x in self.settings.get('audio_languages',legacy)};self.subtitle_langs={general_language(x) for x in self.settings.get('subtitle_languages',legacy)};self.filter_enabled=tk.BooleanVar(value=self.settings.get('filter_enabled',False));self.exe=binary('mkvmerge');self.files=[];self.groups={};self.selected=None;self.widgets={};self.events=queue.Queue();self.running=False
        style=ttk.Style();style.theme_use('clam');style.configure('Treeview',background=PANEL,fieldbackground=PANEL,foreground=FG,rowheight=27,borderwidth=0);style.map('Treeview',background=[('selected','#383838')]);style.configure('Treeview.Heading',background='#252525',foreground=FG);style.configure('TCombobox',fieldbackground='#242424',background='#242424',foreground='#111111')
        menu=tk.Menu(root,tearoff=0,bg=PANEL,fg=FG,activebackground='#383838',activeforeground=FG)
        options=tk.Menu(menu,tearoff=0,bg=PANEL,fg=FG,activebackground='#383838',activeforeground=FG)
        options.add_command(label='Idiomas de áudio...',command=lambda:self.language_options('audio'))
        options.add_command(label='Idiomas de legendas...',command=lambda:self.language_options('subtitles'))
        options.add_separator()
        options.add_command(label='Nomes automáticos de áudio...',command=lambda:self.name_options('audio'))
        options.add_command(label='Nomes automáticos de legendas...',command=lambda:self.name_options('subtitles'))
        options.add_checkbutton(label='Ativar filtro de visualização',variable=self.filter_enabled,command=self.change_filter)
        menu.add_cascade(label='Opções',menu=options)
        menu.add_command(label='Sobre',command=self.show_about)
        root.config(menu=menu)
        header=tk.Frame(root,bg=BG);header.pack(fill='x',padx=18,pady=14)
        tk.Label(header,text='MKV TOOL',font=('Segoe UI',23,'bold'),fg=FG,bg=BG).pack(side='left')
        self.button(header,'Adicionar arquivos',self.add_files).pack(side='right',padx=4)
        self.button(header,'Abrir pasta',self.add_folder).pack(side='right',padx=4)
        self.button(header,'Analisar / agrupar',self.scan).pack(side='right',padx=4)
        bar=tk.Frame(root,bg=BG);bar.pack(fill='x',padx=18)
        self.recursive=tk.BooleanVar(value=False);self.cleanup=tk.BooleanVar(value=True)
        tk.Checkbutton(bar,text='Incluir subpastas',variable=self.recursive,bg=BG,fg=FG,selectcolor=PANEL,activebackground=BG,activeforeground=FG).pack(side='left')
        tk.Checkbutton(bar,text='Remover anexos, botões, capítulos e etiquetas',variable=self.cleanup,bg=BG,fg=FG,selectcolor=PANEL,activebackground=BG,activeforeground=FG).pack(side='left',padx=20)
        self.status=tk.Label(bar,text='Pronto',fg=MUTED,bg=BG);self.status.pack(side='right')
        body=tk.PanedWindow(root,orient='horizontal',bg=BG,sashwidth=6);body.pack(fill='both',expand=True,padx=18,pady=12)
        left=tk.Frame(body,bg=PANEL);right=tk.Frame(body,bg=PANEL);body.add(left,minsize=340);body.add(right,minsize=550)
        tk.Label(left,text='GRUPOS / ARQUIVOS',font=('Segoe UI',12,'bold'),bg=PANEL,fg=FG).pack(anchor='w',padx=12,pady=10)
        self.tree=ttk.Treeview(left,columns=('count',),show='tree headings');self.tree.heading('#0',text='Grupo / arquivo');self.tree.heading('count',text='Total');self.tree.column('#0',width=315);self.tree.column('count',width=55,anchor='center');self.tree.pack(fill='both',expand=True,padx=8,pady=6);self.tree.bind('<<TreeviewSelect>>',self.on_select)
        tk.Label(right,text='FAIXAS DO GRUPO • seleção e ordem',font=('Segoe UI',12,'bold'),bg=PANEL,fg=FG).pack(anchor='w',padx=12,pady=10)
        tk.Label(right,text='Idiomas ocultos serão removidos da saída. Os originais são preservados.',bg=PANEL,fg=MUTED).pack(anchor='w',padx=12)
        columns=('keep','type','codec','lang','default','forced','title')
        self.tracks=ttk.Treeview(right,columns=columns,show='headings',selectmode='browse')
        self.tracks.tag_configure('excluded',foreground='#ff6464')
        self.tracks.tag_configure('default',foreground='#63d889')
        for c,label,width in [('keep','Usar',52),('type','Tipo',85),('codec','Codec',100),('lang','Idioma',90),('default','Padrão',65),('forced','Forçada',65),('title','Nome',150)]:self.tracks.heading(c,text=label);self.tracks.column(c,width=width,stretch=c in ('codec','title'))
        self.tracks.pack(fill='both',expand=True,padx=8,pady=8);self.tracks.bind('<Double-1>',self.toggle)
        controls=tk.Frame(right,bg=PANEL);controls.pack(fill='x',padx=10,pady=6)
        self.button(controls,'Manter / excluir',lambda:self.toggle(None)).pack(side='left',padx=3)
        self.button(controls,'↑ Subir',lambda:self.move(-1)).pack(side='left',padx=3)
        self.button(controls,'↓ Descer',lambda:self.move(1)).pack(side='left',padx=3)
        self.button(controls,'Editar faixa',self.edit).pack(side='left',padx=3)
        self.button(controls,'Organizar automaticamente',self.organize_automatically).pack(side='left',padx=3)
        foot=tk.Frame(root,bg=BG);foot.pack(fill='x',padx=18,pady=12)
        self.output=tk.StringVar(value=self.saved_output);self.output.trace_add('write',self.persist_output);tk.Label(foot,text='Pasta de saída:',bg=BG,fg=FG).pack(side='left');tk.Entry(foot,textvariable=self.output,width=48,bg=PANEL,fg=FG,insertbackground=FG,relief='flat').pack(side='left',padx=8,fill='x',expand=True);self.button(foot,'Escolher pasta...',self.choose_output).pack(side='left',padx=4)
        self.button(foot,'Pré-visualizar',self.preview).pack(side='right',padx=4)
        self.button(foot,'PROCESSAR LOTE',self.process).pack(side='right',padx=4)
        self.log=tk.Text(root,height=6,bg='#101010',fg='#c6cbd8',insertbackground=FG,relief='flat');self.log.pack(fill='x',padx=18,pady=(0,12));self.root.after(120,self.poll)
    def button(self,parent,label,command):return tk.Button(parent,text=label,command=command,bg='#262626',fg='white',activebackground=ACC,activeforeground='white',relief='flat',padx=10,pady=7,cursor='hand2')
    def say(self,s):self.log.insert('end',s+'\n');self.log.see('end')
    def add_files(self):
        paths=filedialog.askopenfilenames(filetypes=[('Matroska','*.mkv')]);self.files=list(dict.fromkeys(self.files+list(map(Path,paths))));self.status.config(text=f'{len(self.files)} arquivos selecionados')
    def add_folder(self):
        d=filedialog.askdirectory()
        if not d:return
        files=Path(d).rglob('*.mkv') if self.recursive.get() else Path(d).glob('*.mkv')
        self.files=list(dict.fromkeys(self.files+list(files)));self.status.config(text=f'{len(self.files)} arquivos selecionados')
    def scan(self):
        if self.running:return
        if not self.exe:return messagebox.showerror('MKVToolNix','Instale o MKVToolNix em C:\\Program Files\\MKVToolNix ou adicione mkvmerge ao PATH.')
        if not self.files:return messagebox.showinfo('Arquivos','Adicione arquivos ou uma pasta primeiro.')
        self.running=True;self.status.config(text='Analisando...');threading.Thread(target=self.scan_worker,daemon=True).start()
    def scan_worker(self):
        groups={};errors=[]
        for p in self.files:
            try:
                tracks=inspect(p,self.exe);sig=signature(tracks)
                if sig not in groups:groups[sig]={'files':[],'tracks':tracks,'plan':[{'id':t['id'],'type':t['type'],'codec':t.get('codec',''),'lang':t.get('properties',{}).get('language_ietf') or t.get('properties',{}).get('language','und'),'default':bool(t.get('properties',{}).get('default_track',False)),'forced':bool(t.get('properties',{}).get('forced_track',False)),'title':t.get('properties',{}).get('track_name',''),'keep':True} for t in tracks]}
                groups[sig]['files'].append(p)
            except Exception as e:errors.append(f'{p.name}: {e}')
        # Cada nova análise usa as faixas originais; alterações não são restauradas do disco.
        self.events.put(('scan',(list(groups.values()),errors)))
    def refresh_groups(self):
        self.tree.delete(*self.tree.get_children())
        for i,g in enumerate(self.groups.values(),1):
            parent=self.tree.insert('', 'end',iid=f'g{i}',text=f'Grupo {i}',values=(len(g['files']),),open=True)
            for j,p in enumerate(g['files']):self.tree.insert(parent,'end',iid=f'f{i}_{j}',text=p.name,values=('',))
    def on_select(self,event):
        sel=self.tree.selection()
        if not sel:return
        item=sel[0];idx=int(item.split('_')[0][1:]);self.selected=idx;self.refresh_tracks()
    def group(self):return self.groups.get(self.selected)
    def refresh_tracks(self):
        self.tracks.delete(*self.tracks.get_children());g=self.group()
        if not g:return
        for i,t in enumerate(g['plan']):
            if self.filter_enabled.get() and t['type'] in ('audio','subtitles') and not self.language_visible(t['lang'],t['type']):continue
            self.tracks.insert('','end',iid=str(i),tags=('excluded',) if not t['keep'] else (('default',) if t['default'] else ()),values=('✓' if t['keep'] else '✕',KINDS.get(t['type'],t['type']),t['codec'],display_language(t['lang']),'Sim' if t['default'] else 'Não','Sim' if t['forced'] else 'Não',t['title']))
    def toggle(self,event):
        g=self.group();sel=self.tracks.selection()
        if g and sel:
            t=g['plan'][int(sel[0])];t['keep']=not t['keep'];self.save_choices();self.refresh_tracks()
    def move(self,step):
        g=self.group();sel=self.tracks.selection()
        if not g or not sel:return
        i=int(sel[0]);j=i+step
        if 0<=j<len(g['plan']):g['plan'][i],g['plan'][j]=g['plan'][j],g['plan'][i];self.save_choices();self.refresh_tracks();self.tracks.selection_set(str(j))
    def edit(self):
        g=self.group();sel=self.tracks.selection()
        if not g or not sel:return
        t=g['plan'][int(sel[0])];win=tk.Toplevel(self.root);win.title('Editar faixa');win.configure(bg=PANEL);win.geometry('370x285');win.transient(self.root);win.grab_set()
        lang=tk.StringVar(value=t['lang']);title=tk.StringVar(value=t['title']);default=tk.BooleanVar(value=t['default']);forced=tk.BooleanVar(value=t['forced'])
        tk.Label(win,text='Idioma (ex.: pt-BR, en, und)',bg=PANEL,fg=FG).pack(anchor='w',padx=15,pady=(12,2))
        tk.Entry(win,textvariable=lang,bg='#252525',fg=FG,insertbackground=FG).pack(fill='x',padx=15)
        tk.Label(win,text='Nome da faixa',bg=PANEL,fg=FG).pack(anchor='w',padx=15,pady=(12,2))
        name_entry=tk.Entry(win,textvariable=title,bg='#252525',fg=FG,insertbackground=FG)
        name_entry.pack(fill='x',padx=15)
        suggestions=[v for v in self.settings.get('name_suggestions_'+t['type'],[]) if isinstance(v,str) and v.strip()]
        # Sugere sem substituir imediatamente o que o usuário está digitando.
        popup=tk.Listbox(win,height=4,bg='#242424',fg=FG,selectbackground='#454545',relief='flat',exportselection=False)
        def close_popup():
            if popup.winfo_manager():popup.place_forget()
        def choose_suggestion(event=None):
            selection=popup.curselection()
            if selection:
                title.set(popup.get(selection[0]));name_entry.icursor('end')
            close_popup();name_entry.focus_set()
            return 'break'
        def suggest(*_):
            typed=title.get().strip().casefold()
            matches=[v for v in suggestions if typed and v.casefold().startswith(typed) and v.casefold()!=typed]
            if not matches:close_popup();return
            popup.delete(0,'end')
            for value in matches:popup.insert('end',value)
            popup.configure(height=min(4,len(matches)))
            popup.place(in_=name_entry,relx=0,rely=1,relwidth=1)
            popup.lift()
        title.trace_add('write',suggest)
        popup.bind('<ButtonRelease-1>',choose_suggestion)
        popup.bind('<Return>',choose_suggestion)
        def accept_tab(event):
            if popup.winfo_manager() and popup.size():
                popup.selection_clear(0,'end');popup.selection_set(0)
                return choose_suggestion()
        name_entry.bind('<Tab>',accept_tab)
        name_entry.bind('<Down>',lambda event:(popup.focus_set(),popup.selection_set(0),'break')[-1] if popup.winfo_manager() and popup.size() else None)
        for label,var in [('Padrão',default),('Forçada',forced)]:tk.Checkbutton(win,text=label,variable=var,bg=PANEL,fg=FG,selectcolor='#252525',activebackground=PANEL).pack(anchor='w',padx=15)
        def save():t.update(lang=lang.get().strip() or 'und',title=title.get(),default=default.get(),forced=forced.get());self.save_choices();self.refresh_tracks();win.destroy()
        self.button(win,'Salvar',save).pack(pady=10)
    def organize_automatically(self):
        if self.running:
            return
        if not self.groups:
            return messagebox.showinfo('Organização automática', 'Analise os arquivos primeiro.')
        win=tk.Toplevel(self.root)
        win.title('Organizar automaticamente')
        win.configure(bg=BG)
        win.geometry('570x390')
        win.transient(self.root)
        win.grab_set()
        tk.Label(win,text='ORGANIZAÇÃO AUTOMÁTICA',font=('Segoe UI',14,'bold'),
                 bg=BG,fg=FG).pack(anchor='w',padx=18,pady=(18,10))
        explanation=('Todos os grupos analisados serão organizados:\\n'
                     '• Vídeo primeiro.\\n'
                     '• Áudio português primeiro e inglês em segundo.\\n'
                     '• Legenda portuguesa primeiro, padrão e forçada.\\n'
                     '• Os demais áudios e legendas serão mantidos após esses.')
        tk.Label(win,text=explanation,justify='left',bg=BG,fg=FG).pack(anchor='w',padx=18)
        convert=tk.BooleanVar(value=bool(self.settings.get('auto_organize_pt_br',False)))
        tk.Checkbutton(win,text='Alterar idiomas portugueses para pt-BR (áudio e legenda)',
                       variable=convert,bg=BG,fg=FG,selectcolor=PANEL,
                       activebackground=BG,activeforeground=FG).pack(anchor='w',padx=18,pady=(14,4))
        tk.Label(win,text='Inclui pt-PT. Apenas a identificação muda, não o idioma falado.\\n'
                 'Atenção: legenda completa marcada como forçada continuará completa.',
                 bg=BG,fg=MUTED,justify='left').pack(anchor='w',padx=18)
        convert_en=tk.BooleanVar(value=True)
        tk.Checkbutton(win,text='Converter en-US para en (áudio e legendas)',
                       variable=convert_en,bg=BG,fg=FG,selectcolor=PANEL,
                       activebackground=BG,activeforeground=FG).pack(anchor='w',padx=18,pady=(4,2))
        def apply():
            if not messagebox.askyesno('Confirmar organização',
                    'Aplicar a organização a todos os grupos analisados?\\n'
                    'As alterações serão usadas apenas nesta sessão e nos arquivos de saída.',
                    parent=win):
                return
            self.settings['auto_organize_pt_br']=convert.get()
            self.persist_settings()
            for g in self.groups.values():
                plan=g['plan']
                for t in plan:
                    if convert.get() and t['type'] in ('audio','subtitles') and general_language(t['lang'])=='pt':
                        t['lang']='pt-BR'
                    if convert_en.get() and t['type'] in ('audio','subtitles') and str(t['lang']).strip().lower().replace('_','-')=='en-us':
                        t['lang']='en'
                videos=[t for t in plan if t['type']=='video']
                audios=[t for t in plan if t['type']=='audio']
                subs=[t for t in plan if t['type']=='subtitles']
                others=[t for t in plan if t['type'] not in ('video','audio','subtitles')]
                pt_audio=[t for t in audios if general_language(t['lang'])=='pt']
                en_audio=[t for t in audios if general_language(t['lang'])=='en']
                remaining_audio=[t for t in audios if general_language(t['lang']) not in ('pt','en')]
                # Prioriza uma legenda já forçada antes de outras em português.
                pt_subs=[t for t in subs if general_language(t['lang'])=='pt']
                pt_subs.sort(key=lambda t:not t['forced'])
                remaining_subs=[t for t in subs if general_language(t['lang'])!='pt']
                for t in videos:
                    t['default']=t is videos[0]
                if pt_audio:
                    for t in audios:t['default']=t is pt_audio[0]
                elif en_audio:
                    for t in audios:t['default']=t is en_audio[0]
                if pt_subs:
                    for t in subs:t['default']=t is pt_subs[0]
                    pt_subs[0]['forced']=True
                g['plan']=videos+pt_audio+en_audio+remaining_audio+pt_subs+remaining_subs+others
            self.refresh_tracks()
            self.say('Organização automática aplicada a todos os grupos analisados.')
            self.status.config(text='Organização automática aplicada. Confira a pré-visualização.')
            win.destroy()
        self.button(win,'Aplicar a todos os grupos',apply).pack(pady=16)

    def name_options(self,track_type):
        label='áudio' if track_type=='audio' else 'legendas'
        key='name_suggestions_'+track_type
        current=self.settings.get(key,[])
        win=tk.Toplevel(self.root);win.title('Nomes automáticos de '+label)
        win.configure(bg=BG);win.geometry('440x520');win.transient(self.root);win.grab_set()
        tk.Label(win,text='Cadastre até 10 nomes de faixas de '+label+'.',bg=BG,fg=FG,font=('Segoe UI',11,'bold')).pack(pady=(18,4))
        tk.Label(win,text='Ao editar uma faixa, digite o início do nome e escolha a sugestão.\nUse Tab para aceitar a primeira sugestão.',bg=BG,fg=MUTED).pack(pady=(0,12))
        entries=[]
        for i in range(10):
            line=tk.Frame(win,bg=BG);line.pack(fill='x',padx=24,pady=3)
            tk.Label(line,text=f'{i+1:02d}',width=3,bg=BG,fg=MUTED).pack(side='left')
            entry=tk.Entry(line,bg='#252525',fg=FG,insertbackground=FG,relief='flat')
            entry.pack(side='left',fill='x',expand=True,ipady=5)
            if i<len(current):entry.insert(0,current[i])
            entries.append(entry)
        def save():
            names=list(dict.fromkeys(e.get().strip() for e in entries if e.get().strip()))
            self.settings[key]=names;self.persist_settings();win.destroy()
        self.button(win,'Salvar nomes',save).pack(pady=16)

    def show_about(self):
        win=tk.Toplevel(self.root)
        win.title('Sobre — MKV Tool')
        win.configure(bg=BG)
        win.geometry('410x375')
        win.resizable(False,False)
        win.transient(self.root)
        win.grab_set()
        win.protocol('WM_DELETE_WINDOW',win.destroy)
        win.update_idletasks()
        x=self.root.winfo_rootx()+(self.root.winfo_width()-410)//2
        y=self.root.winfo_rooty()+(self.root.winfo_height()-375)//2
        win.geometry(f'+{max(0,x)}+{max(0,y)}')

        top=tk.Frame(win,bg=BG)
        top.pack(fill='x',padx=25,pady=(23,13))
        tk.Label(top,text='MKV Tool',font=('Segoe UI',20,'bold'),bg=BG,fg=FG).pack(anchor='w')
        tk.Label(top,text='Organizador de arquivos MKV',font=('Segoe UI',10),bg=BG,fg=MUTED).pack(anchor='w',pady=(3,0))
        tk.Frame(win,bg='#383838',height=1).pack(fill='x',padx=25,pady=(0,14))

        details=tk.Frame(win,bg=BG)
        details.pack(fill='x',padx=25)
        for caption,value in [('Desenvolvedor','Tokon'),('Versão','v1.0.0'),('Plataforma','Windows'),('Licença','MIT (Open Source)')]:
            line=tk.Frame(details,bg=BG)
            line.pack(fill='x',pady=7)
            tk.Label(line,text=caption,font=('Segoe UI',10),bg=BG,fg=MUTED).pack(side='left')
            tk.Label(line,text=value,font=('Segoe UI',10,'bold'),bg=BG,fg=FG).pack(side='right')

        tk.Frame(win,bg='#383838',height=1).pack(fill='x',padx=25,pady=(16,10))
        tk.Label(win,text='© 2026 Tokon — Licenciado sob a licença MIT.',font=('Segoe UI',9),bg=BG,fg=MUTED).pack()
        self.button(win,'Fechar',win.destroy).pack(pady=(14,0),ipadx=20)
        win.bind('<Escape>',lambda event:win.destroy())

    def load_settings(self):
        try:
            obj=json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
            return obj if isinstance(obj,dict) else {}
        except (OSError,ValueError,TypeError):return {}
    def persist_settings(self):
        try:
            CONFIG_PATH.parent.mkdir(parents=True,exist_ok=True)
            CONFIG_PATH.write_text(json.dumps(self.settings,ensure_ascii=False,indent=2),encoding='utf-8')
        except OSError:pass
    def persist_output(self,*_):
        self.settings['output_folder']=self.output.get()
        self.persist_settings()
    def signature_key(self,sig):
        return hashlib.sha256(json.dumps(sig,ensure_ascii=False).encode('utf-8')).hexdigest()
    def save_choices(self):
        # Alterações de faixas valem apenas durante esta sessão.
        # O plano em memória já foi alterado pela interface.
        return

    def language_visible(self,lang,track_type):
        allowed=self.audio_langs if track_type=='audio' else self.subtitle_langs
        return general_language(lang) in allowed
    def change_filter(self):
        self.settings['filter_enabled']=self.filter_enabled.get()
        self.persist_settings();self.refresh_tracks()
    def language_options(self,track_type):
        is_audio=track_type=='audio'
        label='ÁUDIO' if is_audio else 'LEGENDAS'
        saved=self.audio_langs if is_audio else self.subtitle_langs
        win=tk.Toplevel(self.root);win.title('Idiomas de '+('áudio' if is_audio else 'legendas'));win.geometry('520x620')
        win.configure(bg=BG);win.transient(self.root);win.grab_set()
        tk.Label(win,text='IDIOMAS DE '+label,font=('Segoe UI',14,'bold'),bg=BG,fg=FG).pack(anchor='w',padx=16,pady=(15,4))
        tk.Label(win,text='Códigos gerais de 2 letras (ISO 639-1).\\npt inclui pt-BR; en inclui en-US. As faixas mantêm seu idioma original.\\nMarcados: manter. Desmarcados: excluir da saída.\\nSomente '+('áudios' if is_audio else 'legendas')+' serão afetados. Originais preservados.',bg=BG,fg=MUTED,justify='left').pack(anchor='w',padx=16,pady=4)
        container=tk.Frame(win,bg=BG);container.pack(fill='both',expand=True,padx=16)
        canvas=tk.Canvas(container,bg=BG,highlightthickness=0)
        scroll=tk.Scrollbar(container,orient='vertical',command=canvas.yview)
        area=tk.Frame(canvas,bg=BG)
        area.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0),window=area,anchor='nw')
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side='left',fill='both',expand=True);scroll.pack(side='right',fill='y')
        # ISO 639-1 completo; entradas sem código de duas letras ficam acessíveis
        # apenas quando detectadas no arquivo (ex.: 'und').
        found={general_language(t['lang']) for g in self.groups.values() for t in g['plan'] if t['type']==track_type}
        codes=sorted(set(LANGUAGE_NAMES)|found|saved)
        vars={}
        for i,code in enumerate(codes):
            var=tk.BooleanVar(value=code in saved);vars[code]=var
            description=LANGUAGE_NAMES.get(code, 'Indefinido / outro')
            tk.Checkbutton(area,text=f'{code} — {description}',variable=var,bg=BG,fg=FG,
                           selectcolor=PANEL,activebackground=BG,activeforeground=FG,
                           anchor='w').grid(row=i,column=0,sticky='w',padx=8,pady=3)
        def apply():
            chosen={code for code,var in vars.items() if var.get()}
            if is_audio:
                self.audio_langs=chosen;self.settings['audio_languages']=sorted(chosen)
            else:
                self.subtitle_langs=chosen;self.settings['subtitle_languages']=sorted(chosen)
            self.filter_enabled.set(True);self.settings['filter_enabled']=True
            self.persist_settings();self.refresh_tracks();win.destroy()
        self.button(win,'Salvar e aplicar',apply).pack(pady=15)
    def choose_output(self):
        folder=filedialog.askdirectory(title="Escolher pasta de saída")
        if folder:self.output.set(folder)
    def output_for(self,p):
        folder=self.output.get().strip()
        if not folder:raise ValueError('Escolha uma pasta de saída antes de continuar.')
        if not Path(folder).is_absolute():raise ValueError('A pasta de saída precisa ter um caminho completo.')
        return Path(folder)/p.name
    def effective_keep(self,t):
        if not t['keep']:return False
        if self.filter_enabled.get() and t['type'] in ('audio','subtitles'):
            return self.language_visible(t['lang'],t['type'])
        return True
    def command(self,p,g):
        selected=[t for t in g['plan'] if self.effective_keep(t)]
        if not selected:raise ValueError('Grupo sem faixas selecionadas')
        if not any(t['type']=='video' for t in selected):raise ValueError('É necessário manter pelo menos uma faixa de vídeo')
        dest=self.output_for(p)
        if dest.resolve()==p.resolve():raise ValueError('Saída igual à entrada')
        args=[self.exe,'-o',str(dest),'--title','']
        for typ,flag in [('video','--video-tracks'),('audio','--audio-tracks'),('subtitles','--subtitle-tracks')]:
            ids=[str(t['id']) for t in selected if t['type']==typ];args.extend([flag,','.join(ids)] if ids else ['--no-'+{'video':'video','audio':'audio','subtitles':'subtitles'}[typ]])
        args+=['--track-order',','.join(f'0:{t["id"]}' for t in selected)]
        for t in selected:
            id=str(t['id']);args+=['--language',f'{id}:{t["lang"]}','--default-track-flag',f'{id}:{"yes" if t["default"] else "no"}','--forced-display-flag',f'{id}:{"yes" if t["forced"] else "no"}','--track-name',f'{id}:{t["title"]}']
        if self.cleanup.get():args+=['--no-attachments','--no-buttons','--no-chapters','--no-global-tags','--no-track-tags']
        args.append(str(p));return args,dest
    def preview(self):
        if not self.groups:return messagebox.showinfo('Prévia','Analise os arquivos primeiro.')
        if not self.output.get().strip():return messagebox.showwarning('Pasta de saída','Escolha uma pasta de saída primeiro.')
        win=tk.Toplevel(self.root);win.title('Pré-visualização');win.geometry('900x550');area=tk.Text(win,wrap='none');area.pack(fill='both',expand=True)
        for i,g in self.groups.items():
            area.insert('end',f'GRUPO {i} ({len(g["files"])} arquivos)\n')
            for t in g['plan']:area.insert('end',f'  {"MANTER" if self.effective_keep(t) else "REMOVER"} {KINDS.get(t["type"],t["type"])} #{t["id"]} {t["lang"]} {t["codec"]} | padrão={t["default"]} forçada={t["forced"]} nome={t["title"]}\n')
            for p in g['files']:area.insert('end',f'    {p} -> {self.output_for(p)}\n')
            area.insert('end','\n')
        area.configure(state='disabled')
    def process(self):
        if self.running:return
        if not self.groups:return messagebox.showinfo('Lote','Analise os arquivos primeiro.')
        if not self.output.get().strip():return messagebox.showwarning('Pasta de saída','Escolha uma pasta de saída antes de processar.')
        jobs=[]
        try:
            for g in self.groups.values():
                for p in g['files']:
                    args,dest=self.command(p,g)
                    if dest.exists():raise ValueError(f'Saída já existe: {dest}')
                    jobs.append((args,dest,p))
        except Exception as e:return messagebox.showerror('Configuração',str(e))
        if not messagebox.askyesno('Confirmar',f'Processar {len(jobs)} arquivos?\nIdiomas ocultos pelo filtro serão removidos dos arquivos gerados.\nOs originais serão preservados.'):return
        self.running=True;self.status.config(text='Processando...');threading.Thread(target=self.process_worker,args=(jobs,),daemon=True).start()
    def process_worker(self,jobs):
        ok=0
        for n,(args,dest,p) in enumerate(jobs,1):
            try:
                dest.parent.mkdir(parents=True,exist_ok=True)
                r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace',creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
                if r.returncode not in (0,1):raise RuntimeError((r.stderr or r.stdout)[-600:])
                ok+=1;self.events.put(('log',f'[{n}/{len(jobs)}] OK: {p.name}'+(' (avisos)' if r.returncode==1 else '')))
            except Exception as e:self.events.put(('log',f'[{n}/{len(jobs)}] ERRO: {p.name}: {e}'))
        self.events.put(('done',f'Concluído: {ok}/{len(jobs)} arquivos.'))
    def poll(self):
        try:
            while True:
                kind,data=self.events.get_nowait()
                if kind=='scan':
                    groups,errors=data;self.groups={i:g for i,g in enumerate(groups,1)};self.selected=None;self.refresh_groups();self.status.config(text=f'{len(groups)} grupos • {sum(len(g["files"]) for g in groups)} arquivos');self.say(f'Análise concluída: {len(groups)} grupos.');[self.say('ERRO: '+e) for e in errors];self.running=False
                elif kind=='log':self.say(data)
                elif kind=='done':
                    self.say(data);self.status.config(text=data);self.running=False
                    try:
                        import winsound
                        winsound.MessageBeep(winsound.MB_ICONASTERISK)
                    except (ImportError,RuntimeError,OSError):
                        self.root.bell()
        except queue.Empty:pass
        self.root.after(120,self.poll)

if __name__=='__main__':
    root=tk.Tk();App(root);root.mainloop()
