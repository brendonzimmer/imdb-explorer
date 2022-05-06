# Brendon Zimmer
# ITP 116, 11:00-11:50
# Final Project — Movie Finder and Explorer

import requests
from tkinter import *
from io import BytesIO
from PIL import ImageTk, Image

API_KEY = "k_t3f76pdi"

def detailsWindow(movie: dict, parent: Tk):
    state = []
    root = Tk()
    root.title(movie['fullTitle'])
    root.geometry("500x500")

    # root = Toplevel(parent)
    # root.title(f'{movie["fullTitle"]} Details')
    # root.geometry("800x500")

    # rootFrame = Frame(root)
    # rootFrame.place(relx=.5, rely=.5, anchor=CENTER)

    # movieFrame = Frame(rootFrame)
    # movieFrame.grid()
            
    # root.mainloop()

def details(id: str, parent: Tk):
    res = requests.get(f"https://imdb-api.com/en/API/Title/{API_KEY}/{id}/Images,Ratings")
    
    if res.status_code != 200:
        print("\nError:", res.status_code)
    elif not res.json()['id']:
        print(f"\nError: {res.json()['errorMessage']}")
        return
    else:
        movie = res.json()
        detailsWindow(movie, parent)


def previewWindow(movie: dict):
    state = []
    root = Tk()
    root.title('Movie Preview')
    root.geometry("520x600")

    rootFrame = Frame(root)
    rootFrame.place(relx=.5, rely=.5, anchor=CENTER)

    previewFrame = Frame(rootFrame)
    previewFrame.grid()
    
    jpg = Image.open(BytesIO(requests.get(movie['image'].replace("original", "336x462")).content))
    bytes = ImageTk.PhotoImage(jpg)
    state.append(bytes)
    thumbnail = Label(previewFrame, image=bytes)
    thumbnail.grid(row=0)

    try: title = Label(previewFrame, text=movie['fullTitle'])
    except: title = Label(previewFrame, text=movie['title']+" "+movie['description'])
    title.config(font="Arial 24 bold")
    title.grid(row=1)

    moreInfo = Button(previewFrame, text="View More", command=lambda: details(movie['id'], parent=root))
    moreInfo.grid(row=2)

    root.mainloop()


def preview(data: dict):
    print()
    
    while True:
        inp = input("View a title (enter # or 'done'): ")
        
        if "done" in inp.lower(): break

        if inp.isdigit(): inp = int(inp)
        
        if inp <= 0 or inp > len(data): continue
        
        previewWindow(data[int(inp)-1])


def search(title: str):
    print("May take a minute. To speed up, try searching for a title with a year.")
    print("Searching...")
    res = requests.get(f"https://imdb-api.com/en/API/SearchMovie/{API_KEY}/{title}")
            
    if res.status_code != 200:
        print("\nError:", res.status_code)
    elif not res.json()['results']:
        print(f"\nError: {res.json()['errorMessage']}")
        return
    else:
        data = res.json()['results']
        print("\nResults:")

        for i, movie in enumerate(data): print(f"\t{i+1}. {movie['title']} {movie['description']}")
        preview(data)


def top100():
    res = requests.get(f"https://imdb-api.com/en/API/MostPopularMovies/{API_KEY}")
            
    if res.status_code != 200:
        print("\nError:", res.status_code)
    elif len(res.json()['items']) == 0:
        print(f"\nError: {res.json()['errorMessage']}")
        return
    else:
        data = res.json()['items']
        for movie in data: print(f"\t{movie['rank']}: {movie['fullTitle']}")
        preview(data)


def menu():
    while True:
        print("Menu Items:")
        print("\t1. View top 100 most popular movies")
        print("\t2. Search a title")
        print("\t3. Quit")
        choice = input("What would you like to do? ")

        if choice == "1":
            print("\nTop 100 most popular movies:")
            top100()
            
        if choice == "2":
            title = input("\nEnter a title: ")
            search(title)

        if choice == "3":
            print("\nThank you for using IMDb explorer!")
            break

        print("\n-------\n")


def main():
    print("Welcome to the IMDb explorer!")
    menu()


main()