
def get_node_js_tracking_code(api_endpoint_url: str) -> str:
    return """
            router.get('""" + api_endpoint_url + """', function(req, res){
            console.log("FILE OPENEDWWWW!!!!");
            fs.readFile('./www.trony.it/www.trony.it/online/web/WFS/Trony-B2C-Site/it_IT/-/EUR/ViewPuntiVendita-Mapsd8b1.html',function(error, content){
                if(error){
                    res.writeHead(500);
                    res.end();
                } else {
                    res.writeHead(200, { 'Content-type': 'text/html' });
                    res.end(content, 'utf-8');
                }
            });
        });
    """