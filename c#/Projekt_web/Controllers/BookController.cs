using Projekt_web.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace Projekt_web.Controllers
{
    public class BookController : Controller
    {
        public ActionResult ViewAll()
        {
            List<Book> books;
            using (DatabaseContext db = new DatabaseContext())
                books = db.Books.ToList();

            return View(books);
        }

        public ActionResult View(int id)
        {
            Book book;
            using (DatabaseContext db = new DatabaseContext())
                book = db.Books.FirstOrDefault(a => a.BookId == id);

            return View(book);
        }

    }
}