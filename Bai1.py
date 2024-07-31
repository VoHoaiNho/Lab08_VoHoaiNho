import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename

class Notepad:
    __root = Tk()

    # Đặt kích thước mặc định cho cửa sổ
    __thisWidth = 3000
    __thisHeight = 300
    # Khu vực văn bản chính
    __thisTextArea = Text(__root)
    # Thanh menu
    __thisMenuBar = Menu(__root)
    # Menu File
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    # Menu Edit
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    # Menu Help
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)

    # Thanh cuộn cho khu vực văn bản
    __thisScrollBar = Scrollbar(__thisTextArea)
    # Tên file hiện tại
    __file = None

    def __init__(self, **kwargs):
        try:
            self.__root.wm_iconbitmap("Notepad.ico")
        except:
            pass

        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # Đặt tiêu đề cửa sổ
        self.__root.title("Untitled - Notepad")

        # Lấy kích thước màn hình
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        # Tính toán vị trí cửa sổ để đặt giữa màn hình
        left = (screenWidth / 2) - (self.__thisWidth / 2)
        top = (screenHeight / 2) - (self.__thisHeight / 2)

        # Đặt kích thước và vị trí cửa sổ
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight, left, top))

        # Cấu hình lưới cho khu vực văn bản
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Đặt khu vực văn bản vào lưới
        self.__thisTextArea.grid(sticky=N + E + S + W)

        # Thêm các lệnh vào menu File
        self.__thisFileMenu.add_command(label="New", command=self.__newFile)
        self.__thisFileMenu.add_command(label="Open", command=self.__openFile)
        self.__thisFileMenu.add_command(label="Save", command=self.__saveFile)
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit", command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)

        # Thêm các lệnh vào menu Edit
        self.__thisEditMenu.add_command(label="Cut", command=self.__cut)
        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)

        # Thêm lệnh vào menu Help
        self.__thisHelpMenu.add_command(label="About Notepad", command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help", menu=self.__thisHelpMenu)

        # Cấu hình menu bar
        self.__root.config(menu=self.__thisMenuBar)

        # Đặt thanh cuộn vào khu vực văn bản
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __quitApplication(self):
        # Đóng ứng dụng
        self.__root.destroy()

    def __showAbout(self):
        # Hiển thị thông tin về Notepad
        showinfo("Notepad", "Notepad by OpenAI")

    def __openFile(self):
        # Mở file và hiển thị nội dung trong khu vực văn bản
        self.__file = askopenfilename(defaultextension=".txt",
                                      filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

        if self.__file == "":
            self.__file = None
        else:
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea.delete(1.0, END)

            file = open(self.__file, "r")
            self.__thisTextArea.insert(1.0, file.read())
            file.close()

    def __newFile(self):
        # Tạo file mới
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __saveFile(self):
    # Lưu file
        if self.__file is None:  # Kiểm tra xem file hiện tại có đang được mở không
            self.__file = asksaveasfilename(initialfile='Untitled.txt',
                                        defaultextension=".txt",
                                        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        # Nếu file chưa được mở, hiển thị hộp thoại lưu file và lấy tên file

            if self.__file == "":  # Nếu không có tên file nào được chọn
                self.__file = None  # Đặt tên file là None
            else:
                file = open(self.__file, "w")  # Mở file ở chế độ ghi
                file.write(self.__thisTextArea.get(1.0, END))  # Ghi nội dung từ khu vực văn bản vào file
                file.close()  # Đóng file

            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            # Cập nhật tiêu đề cửa sổ với tên file vừa lưu

        else:
            file = open(self.__file, "w")  # Nếu file đã được mở, mở file ở chế độ ghi
            file.write(self.__thisTextArea.get(1.0, END))  # Ghi nội dung từ khu vực văn bản vào file
            file.close()  # Đóng file

    def __cut(self):
        # Cắt văn bản
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        # Sao chép văn bản
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        # Dán văn bản
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):
        # Bắt đầu vòng lặp chính của ứng dụng
        self.__root.mainloop()


# Khởi tạo và chạy ứng dụng Notepad
notepad = Notepad(width=600, height=400)
notepad.run()
