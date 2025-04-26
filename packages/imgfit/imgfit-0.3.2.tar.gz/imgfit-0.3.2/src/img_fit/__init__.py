from PIL import Image
import matplotlib

__version__ = "0.3.2"

def add_fitter(img, fit_img, output_img) -> Image.Image:
    import math

    flag = Image.open(fit_img)
    file = img
    if file:
        head = Image.open(file)
        width, height = flag.size
        flag2 = flag.crop((66, 0, height+66, height))
        for i in range(height):
            for j in range(height):
                color = flag2.getpixel((i, j))
                distance = int(math.sqrt(i**2+j**2))
                alpha = 255-distance//4
                if alpha<0:
                    alpha = 0
                new_color = color[0:-1]+(alpha, )
                flag2.putpixel((i, j), new_color)
        flag_new = flag2.resize(head.size)
        head.paste(flag_new, (0, 0), flag_new)
        head.save(output_img)
    return head

def text_painting(img, char:list, output:str=None) -> str:
    img = Image.open(img)
    img = img.resize((60,60))
    img = img.convert('L')
    txt = ''
    for i in range(60):
        for j in range(60):
            txt += char[int(len(char) * (img.getpixel((j,i)) / 256))]
        txt += "\n"
    if output is not None:
        result=open(output,"w")
        result.write(txt)
        result.close()
    else:
        print(txt)
    return txt

def latex2text(text, output=None):
    if output is None:
        from pylatexenc.latex2text import LatexNodes2Text
        converter = LatexNodes2Text()
        latex_str = text
        readable_str = converter.latex_to_text(latex_str)
        print(readable_str)  # 输出：E = mc²
    else:
        from matplotlib import mathtext
        mathtext.math_to_image(text, output, dpi=300) 

def create_image(red:int, green:int, blue:int, width:int, height:int, alpha:int = 100, output_image=None) -> Image.Image:
    """
    Create a new image.
    
    :params float red: Image depth of red.
    :params float green: Image depth of green.
    :params float blue: Image depth of blue.
    :params float alpha=1: Image depth of alpha.
    :params int width: Image width.
    :params int height: Image height.
    
    :return Image: The created image
    """

    image = Image.new('RGBA', (width, height), (red, green, blue, alpha))
    if output_image is not None:
        image.save(output_image)
    return image

def main():
    import argparse
    import img_fit

    class OutputAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            self.handle_output(parser, namespace, values)

        @staticmethod
        def handle_output(parser, namespace, values):
            setattr(namespace, "output", values) 

    parser = argparse.ArgumentParser(description="img_fit commands")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_text = subparsers.add_parser("text", help="Get the image text")
    p_text.add_argument("from_img", help="The image you want to change",type=str) 
    p_text.add_argument("chars", nargs="+", help="The chars ypu want to make a text painting.",type=str) 
    p_text.add_argument("-o","--output",action=OutputAction,type=str,help="The output path.")  

    subparsers.add_parser("version", help="Get the version.")

    p_fitter = subparsers.add_parser("fitter", help="Fitter the image.")
    p_fitter.add_argument("from_img",help="The image you want to change",type=str)
    p_fitter.add_argument("fitter_img",help="The fitter image.",type=str)
    p_fitter.add_argument("output_img",help="The output image path.",type=str)

    p_latex = subparsers.add_parser("latex", help="Get the text latex.")
    p_latex.add_argument("text",help="The image you want to change",type=str)
    p_latex.add_argument("-o","--output",action=OutputAction,type=str,help="The output path.")  

    p_create = subparsers.add_parser("create", help="Create a new image.")
    p_create.add_argument("img",help="The image you want to change",type=str)
    p_create.add_argument("r",help="Image depth of red.",type=int)
    p_create.add_argument("g",help="Image depth of green.",type=int)
    p_create.add_argument("b",help="Image depth of blue.",type=int)
    p_create.add_argument("width",help="Image width.",type=int)
    p_create.add_argument("height",help="Image height.",type=int)
    p_create.add_argument("a",help="Image depth of alpha.",type=float,default=1,nargs="?")

    args = parser.parse_args()
    try:
        if args.command == "text":
            img_fit.text_painting(args.from_img,args.chars,args.output)
        elif args.command == "fitter":
            img_fit.add_fitter(args.from_img,args.fitter_img,args.output_img)
        elif args.command == "latex":
            img_fit.latex2text(args.text,args.output)
        elif args.command == "create":
            img_fit.create_image(args.r,args.g,args.b,args.width,args.height,args.a,args.img)
        elif args.command == "version":
            print(f'version:imgfit {img_fit.__version__}')
    except FileNotFoundError as fe:
        print("Error:",fe)

if __name__ == "__main__":
    main()