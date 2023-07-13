using Projekt_web.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace Projekt_web.Controllers
{
    public class UserController : Controller
    {
        public ActionResult Rent(int? id)
        {
            Book book;
            using (DatabaseContext db = new DatabaseContext())
                book = db.Books.FirstOrDefault(x => x.BookId == id);

            return View(book);
        }

        [HttpPost, ActionName("Rent")]
        public ActionResult RentConfirm(int? id)
        {
            using (DatabaseContext db = new DatabaseContext())
            {
                Book book = db.Books.FirstOrDefault(x => x.BookId == id);
                db.RentedBooks.Add(new RentedBook(1, 1, 1, DateTime.Now));
                book.Available = false;

                db.SaveChanges();
            }

            return RedirectToAction("ViewAll");
        }

        public ActionResult Return(int? id)
        {
            RentedBook book;
            using (DatabaseContext db = new DatabaseContext())
                book = db.RentedBooks.FirstOrDefault(x => x.BookId == id);

            return View(book);
        }

        [HttpPost, ActionName("Return")]
        public ActionResult ReturnConfirm(int? id)
        {
            using (DatabaseContext db = new DatabaseContext())
            {
                RentedBook rentedBook = db.RentedBooks.FirstOrDefault(x => x.BookId == id);
                db.RentedBooks.Remove(rentedBook);
                Book book = db.Books.FirstOrDefault(x => x.BookId == id);
                book.Available = true;
                db.SaveChanges();
            }

            return RedirectToAction("ViewAll");
        }
    }
}