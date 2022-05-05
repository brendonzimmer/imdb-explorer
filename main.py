# Brendon Zimmer
# ITP 116, 11:00-11:50
# Final Project — Movie Finder and Explorer

import requests
from tkinter import *
from io import BytesIO
from PIL import ImageTk, Image
# import json

API_KEY = "k_t3f76pdi"

def search(title: str):
    print("Searching...")
    print("May take a minute. To speed up, try searching for a title with a year.")

    res = requests.get(f"https://imdb-api.com/en/API/SearchMovie/k_t3f76pdi/{title}")
            
    if res.status_code != 200:
        print("Error:", res.status_code)
    else:
        # print(json.dumps(res.json(), indent=4))
        data = res.json()['results']
        if data is None:
            print(f"\nError: {res.json()['errorMessage']}")
            return

        ids = []
        
        print("\nResults:")
        for i, movie in enumerate(data):
            print(f"\t{i+1}. {movie['title']} {movie['description']}")
            ids.append(movie['id'])

        choice = input("\nWhich movie would you like to see? ")
        print(f"You want to see {ids[int(choice)-1]}: \"{data[int(choice)-1]['title']}\" ")
        print("\nComing Soon!")


def detailsDisplay(movie: dict, thumbnail: str, images: list, movieFrame: Frame):
    jpg = Image.open(BytesIO(requests.get(thumbnail[0:thumbnail.find("@.")] + "@._V1_UX192_CR0,3,192,264.jpg").content))
    bytes = ImageTk.PhotoImage(jpg)
    thumbnail = Label(movieFrame, image=bytes)
    thumbnail.grid(row=0, column=0)

    images.append(bytes)

    title = Label(movieFrame, text=movie['fullTitle'])
    title.config(font="Arial 24 bold")
    title.grid(row=1, column=0)


def detailsWindow(parent: Tk, movie: dict):
    movieDetails = getMovieDetails(movie['id'])
    if movieDetails is None:
        print(f"Error: No movie details found for {movie['id']}.")
        return
    
    images = []

    root = Toplevel(parent)
    root.title(f'{movie["fullTitle"]} Details')
    root.geometry("800x500")

    rootFrame = Frame(root)
    rootFrame.place(relx=.5, rely=.5, anchor=CENTER)

    movieFrame = Frame(rootFrame)
    movieFrame.grid()
            
    detailsDisplay(movieDetails, movie['image'], images, movieFrame)
    root.mainloop()


def getMovieDetails(id: str):
    res = requests.get(f"https://imdb-api.com/en/API/Title/k_t3f76pdi/{id}/Images,Ratings")
    
    if res.status_code != 200:
        print("Error:", res.status_code)
    else:
        # print(json.dumps(res.json(), indent=4))
        if res.json()['id'] is None:
            print(f"\nError: {res.json()['errorMessage']}")
            return
        
        return res.json()


def moviesDisplay(data: list, images: list, moviesFrame: Frame, offset:int=0, *, root):
    for child in moviesFrame.winfo_children(): child.destroy()

    back_offset = offset - 4
    next_offset = offset + 4
    
    backButton = Button(moviesFrame, text="<", command=lambda: moviesDisplay(data, images, moviesFrame, back_offset, root=root))
    backButton.grid(row=0, column=0)

    nextButton = Button(moviesFrame, text=">", command=lambda: moviesDisplay(data, images, moviesFrame, next_offset, root=root))
    nextButton.grid(row=0, column=3)

    for i, movie in enumerate(data[offset:offset+4]):

        print(f"\t{movie['rank']}: {movie['fullTitle']}")
        
        componentFrame = Frame(moviesFrame)
        componentFrame.grid(row=(i%4)//2, column=(i%2)+1)


        # print(movie['image'])
        jpg = Image.open(BytesIO(requests.get(movie['image'][0:movie['image'].find("@.")] + "@._V1_UX192_CR0,3,192,264.jpg").content)) # They just changed the API while making this :( see if it changes back
        bytes = ImageTk.PhotoImage(jpg)
        thumbnail = Label(componentFrame, image=bytes)
        thumbnail.grid(row=0, column=i)

        images.append(bytes)

        title = Label(componentFrame, text=f"{movie['rank']}: {movie['title']}")
        title.config(font="Arial 16")
        title.grid(row=1, column=i)

        moreInfo = Button(componentFrame, text="More Info!", command=lambda: detailsWindow(root, data[offset+i]))
        moreInfo.grid(row=2, column=i)


def moviesWindow(data: list):
    images = []

    root = Tk()
    root.title("Top 100 Most Popular Movies")
    root.geometry("1000x700")

    rootFrame = Frame(root)
    rootFrame.place(relx=.5, rely=.5, anchor=CENTER)

    moviesFrame = Frame(rootFrame)
    moviesFrame.grid()
            
    moviesDisplay(data, images, moviesFrame, root=root)
    mainloop()


def top100():
    res = requests.get("https://imdb-api.com/en/API/MostPopularMovies/k_t3f76pdi")
            
    if res.status_code != 200:
        print("Error:", res.status_code)
    else:
        # print(json.dumps(res.json(), indent=4))
        data = res.json()['items']
        if len(data) == 0:
            print(f"\nError: {res.json()['errorMessage']}")
            return

        moviesWindow(data)


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
            print("\nGoodbye!")
            break

        print("\n-------\n")


def main():
    print("Welcome to the IMDb explorer!")
    menu()


main()