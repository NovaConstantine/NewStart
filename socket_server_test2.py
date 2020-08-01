import socket
import urllib.parse
import time
host = '172.24.11.241'

port = 1502


class Request():
    def __init__(self):
        self.path = ''
        self.query = {}
        self.method ='get'        
        self.body = ''

    def form(self):
        body = urllib.parse.unquote(self.body)
        log('body is',body)
        args = body.split('&')
        f = {}
        for arg in args:
            k,v = arg.split('=')
            f[k] = v

        return f
    

class Message(object):
    def __init__(self):
        self.message = ''
        self.author = ''

    def __repr__(self):
        return '{}:{}'.format(self.author,self.message)

def template(filename):
    with open('templates/'+filename , 'r',encoding ='utf-8') as f:
        return f.read()

def parsed_path(path):
    index = path.find('?')
    if index == -1:
        return path,{}

    else:
        path, query_s = path.split('?',1)
        args = query_s.split('&')
        query = {}
        for arg in args:
            k,v = arg.split('=')

def response_for_path(path):
    #print('test3',path)
    path,query = parsed_path(path)
    #print('test4',path,query)
    request.path = path
    request.query = query
    log('path and query',path, query)
    #print('test1:',path)
    r = {
        '/':route_index,
        '/ice': route_index_ice,
        '/img/ice.jpg':route_img_ice,
        '/message': route_message,        
        
        }
    response = r.get(path,error)
    return response()


def route_index():
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'

    body = '<h1>Hello World!</h1>\r\n<h2>The brave may not live forever, but the cautious do not live at all.</h2><h3>人生如逆旅，我亦是行人</h3>'
    r= header +'\r\n' +body
    return r.encode('utf-8')

def route_index_ice():
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'

    body = '<h1>Hello World!</h1><img src="img/ice.jpg"/>'
    r= header +'\r\n' +body
    return r.encode('utf-8')


def route_img_ice():
    with open('ice.jpg','rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image\r\n\r\n'
        img = header + f.read()
        return img


def route_message():
    if request.method == 'POST':
        msg = Message()
        form = request.form()
        
        msg.author = form.get('author','')
        msg.message = form.get('message','')
        message_list.append(msg)
                

    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('message.html')
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{message}}',msgs)

    r = header +'\r\n' +body
    return r.encode('utf-8')


def error(code = 404):
    error_dict = {404: b'HTTP/1.1 404 Not Found\r\n<h1>404 Not Found</h1>',
                    405:b'',
                    }
    
    return error_dict.get(code,b'')

def log(*arg,**args):
    print(*arg,**args)


request = Request()        

with open('templates/message.txt','r',encoding = 'utf-8') as f:
    message_list = f.read().strip().split('\n')
print(message_list)

def run(host = '',port = 1502):    
    with socket.socket() as web:
        web.bind((host,port))
        web.listen(5)
        print('开启循环')


        while True:
            
            conn,addr = web.accept()
            
            data = conn.recv(2048).decode('utf-8')
            try:
                print('1,',data)
                request.method = data.split()[0]
                request.body = data.split('\r\n\r\n')[1]
                path = data.split()[1]
                response = response_for_path(path)
                conn.sendall(response)
                if len(data)>0:
                    #print('writing')
                    with open('templates/message.txt','w+', encoding = 'utf-8') as f:
                        f.write('\n'.join([str(m) for m in message_list]))

            except Exception as e:
                log('error',e)
                #print('Wrong!', e)
            conn.close()
            time.sleep(0.1)
if __name__ == '__main__':
    config = dict(host = host,port = 1502)
    run(**config)


