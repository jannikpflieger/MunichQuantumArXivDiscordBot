import urllib.request
import os

arxiv_categories = [
    # Physics
    "astro-ph", "astro-ph.CO", "astro-ph.EP", "astro-ph.GA", "astro-ph.HE", "astro-ph.IM", "astro-ph.SR",
    "cond-mat", "cond-mat.dis-nn", "cond-mat.mes-hall", "cond-mat.mtrl-sci", "cond-mat.other", "cond-mat.quant-gas", "cond-mat.soft", "cond-mat.stat-mech", "cond-mat.str-el", "cond-mat.supr-con",
    "gr-qc",
    "hep-ex",
    "hep-lat",
    "hep-ph",
    "hep-th",
    "math-ph",
    "nlin", "nlin.AO", "nlin.CG", "nlin.CD", "nlin.SI", "nlin.PS",
    "nucl-ex",
    "nucl-th",
    "physics", "physics.acc-ph", "physics.ao-ph", "physics.atom-ph", "physics.atm-clus", "physics.bio-ph", 
    "physics.chem-ph", "physics.class-ph", "physics.comp-ph", "physics.data-an", "physics.ed-ph", "physics.flu-dyn", "physics.gen-ph", "physics.geo-ph", "physics.hist-ph", "physics.ins-det", "physics.med-ph", "physics.optics", "physics.plasm-ph", "physics.pop-ph", "physics.soc-ph", "physics.space-ph",
    "quant-ph",
    
    # Mathematics
    "math", "math.AG", "math.AT", "math.AP", "math.CT", "math.CA", "math.CO", 
    "math.AC",
    "math.CV", "math.DG", "math.DS", "math.FA", "math.GM", "math.GN", "math.GT", "math.HO", "math.IT", 
    "math.KT", 
    "math.LO", "math.MP", 
    "math.MG", 
    "math.NT", "math.NA", "math.OA", "math.OC", "math.PR", "math.QA", "math.RT", "math.RA", "math.SP", "math.ST", "math.SG",

    # Computer Science
    "cs", "cs.AI", "cs.CL", "cs.CC", "cs.CE", "cs.CG", "cs.GT", "cs.CV", "cs.CY", "cs.CR", "cs.DS", "cs.DB", "cs.DL", "cs.DM", "cs.DC", "cs.ET", "cs.FL", "cs.GL", "cs.GR", "cs.HC", "cs.IR", "cs.IT", "cs.LG", "cs.LO", "cs.MS", "cs.MA", "cs.NI", "cs.NE", "cs.PF", "cs.PL", "cs.RO", "cs.SI", "cs.SE", "cs.SD", "cs.SC"
]

for categorie in arxiv_categories:
    base_url = 'http://export.arxiv.org/api/query?'
    
    query_params = {
        'search_query': f'all:{categorie}',  
        'start': 0,                     
        'max_results': 1000,              
        'sortBy': 'submittedDate',      
        'sortOrder': 'descending'  
    }
    
    query_url = base_url + urllib.parse.urlencode(query_params)
    try:
        response = urllib.request.urlopen(query_url)
    except Exception as e:
        print(f"Error: {e}")
        continue
    
    try:
        xml_data = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error: {e}")
        continue
    
    categorie_s = categorie.replace(".", "_")

    output_file = f"arxiv_recent_entries_{categorie_s}.atom"
    output_folder = "arxiv_entries"
    
    with open(os.path.join(output_folder, output_file), "w", encoding="utf-8") as file:
        file.write(xml_data)
    
    print(f"Saved the entries to {output_file}")
    print(f"Number of entries: {xml_data.count('<entry>')}")
    print("-" * 40)
