import struct
from obj import Obj

ancho = int(input("Ingrese el ancho de la imagen\n"))
alto = int(input("Ingrese el alto de la imagen\n"))

#xInicial = float(input("Ingrese el parametro de -1 a 1 de la coordenada inicial de x de la linea\n"))
#xFinal = float(input("Ingrese el parametro de -1 a 1 de la coordenada final de x de la linea\n"))

#yInicial = float(input("Ingrese el parametro de -1 a 1 de la coordenada inicial de y de la linea\n"))
#yFinal = float(input("Ingrese el parametro de -1 a 1 de la coordenada final de y de la linea\n"))

#xvertex = float(input("Ingrese el parametro de -1 a 1 de x de  glVertex\n"))
#yvertex = float(input("Ingrese el parametro de -1, a 1 de y glVertex\n"))

print("Ingresa el color con el que llenaras el mapa de bits, parametros 0 a 1\n")
redI = float(input("Ingresa el color red\n"))
greenI = float(input("Ingresa el color green\n"))
blackI = float(input("Ingresa el color black\n"))
      
print("Ingresa el color con el que pintaras, parametros 0 a 1\n")      
red = float(input("Ingresa el color red\n"))
green = float(input("Ingresa el color green\n"))
black = float(input("Ingresa el color black\n"))

def char(c):
  # char
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  # short
  return struct.pack('=h', w)

def dword(w):
  # long
  return struct.pack('=l', w)


def color(r, g, b):
  return bytes([b, g, r])

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

class Renderer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.clear()

  def clear(self):
    self.framebuffer = glClear()
    
  def write(self, filename):
    f = open(filename, 'bw')

    # file header 14
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + 3*(self.width*self.height)))
    f.write(dword(0))
    f.write(dword(14 + 40))

    # info header 40
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(3*(self.width*self.height)))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    
    # bitmap
    for y in range(self.height):
      for x in range(self.width):
        f.write(self.framebuffer[y][x])

    f.close()
  
  def render(self, nombre):
    self.write(nombre +'.bmp')

  def point(self, x, y, color = None):
    self.framebuffer[int(y)][int(x)] = color or self.current_color

  def line(self, x0, y0, x1, y1):
      dy = abs(y1 - y0)
      dx = abs(x1 - x0)

      steep = dy > dx

      if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

      offset = 0 * 2 * dx
      threshold = 0.5 * 2 * dx
      y = y0

      # y = mx + b
      points = []
      for x in range(x0, x1):
        if steep:
          points.append((y, x))
        else:
          points.append((x, y))

        offset += (dy/dx) * 2 * dx
        if offset >= threshold:
          y += 1 if y0 < y1 else -1
          threshold += 1 * 2 * dx

      for point in points:
          r.point(*point)

  def load(self, filename, translate, scale):
    model = Obj(filename)
    
    for face in model.faces:
      vcount = len(face)
      for j in range(vcount):
        f1 = face[j][0]
        f2 = face[(j + 1) % vcount][0]

        v1 = model.vertices[f1 - 1]
        v2 = model.vertices[f2 - 1]

        x1 = round((v1[0] + translate[0]) * scale[0])
        y1 = round((v1[1] + translate[1]) * scale[1])
        x2 = round((v2[0] + translate[0]) * scale[0])
        y2 = round((v2[1] + translate[1]) * scale[1])
        
        self.line(x1, y1, x2, y2)
  
      
      
#funciones implementadas
def  glInit():
    pass

def glCreateWindow(width, height):
    return  Renderer(width, height)

def  glViewPort(x, y, width, height):
    return ([x, y, width, height])

def glClear():
    return[
      [colorI for x in range(ancho)]
      for y in range(alto)
    ]
  
def glClearColor(r, g, b):
    r = int(r * 255) 
    g = int(g * 255)
    b = int(b * 255)
    return bytes([b, g, r])

def glVertex(x, y):
    if(x>0):
        xw = int((x+1) * (vw[2]/2)  + vw[0]) - 1
        
    else:
        xw = int((x+1) * (vw[2]/2)  + vw[0])

        
    if(y>0):
        yw = int((y+1) * (vw[3]/2) + vw[1]) -1
        
    else:
        yw = int((y+1) * (vw[3]/2) + vw[1]) 
        
        
        
    return ([xw, yw])
               
def  glColor(r, g, b):
    r = int(r * 255) 
    g = int(g * 255)
    b = int(b * 255)
    return bytes([b, g, r])
    
def  glFinish():
    nombreImagen = input("Ingrese el nombre de la Imagen\n")
    return nombreImagen


def glLine(x0, y0, x1, y1):
    
    if(x0>0):
        x0 = int((x0+1) * (vw[2]/2)  + vw[0]) - 1
            
    else:
        x0 = int((x0+1) * (vw[2]/2)  + vw[0])
            
    if(y0>0):
        y0 = int((y0+1) * (vw[3]/2) + vw[1]) -1
        
    else:
        y0 = int((y0+1) * (vw[3]/2) + vw[1]) 
    
    if(x1>0):
        x1 = int((x1+1) * (vw[2]/2)  + vw[0]) - 1
            
    else:
        x1 = int((x1+1) * (vw[2]/2)  + vw[0])
            
    if(y1>0):
        y1 = int((y1+1) * (vw[3]/2) + vw[1]) -1
        
    else:
        y1 = int((y1+1) * (vw[3]/2) + vw[1]) 
    

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    
    steep = dy > dx

    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    offset = 0
    threshold = 0.5
    m = dy/dx
    y = y0

    for x in range(x0, x1 + 1):
        if steep:
            r.point(y, x, colorpintado)
        else:
            r.point(x, y, colorpintado)

        offset += m
        if offset >= threshold:
            y += 1 if y0 < y1 else -1
            threshold  += 1


      
colorI = glClearColor(redI, greenI, blackI)
colorpintado = glColor(red, green, black)
r = glCreateWindow(ancho, alto)
#vw = glViewPort(0, 0, ancho, alto)
#colorpunto = glVertex(xvertex, yvertex)
#r.point(colorpunto[0],colorpunto[1], colorpintado)
r.load('./cube.obj', [4,-2], [100,100])
nombre = glFinish()
r.render(nombre)