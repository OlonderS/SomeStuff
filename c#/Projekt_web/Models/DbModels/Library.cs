using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web;

namespace Projekt_web.Models.DbModels
{
    public class Library
    {
        public int LibraryId { get; set; }
        public string Name { get; set; }
        public List<Book> Books { get; set; }
        public List<User> Users { get; set; }

        static Library()
        {
            List<Book> Books = new List<Book>();
        }
        public override string ToString()
        {
            StringBuilder sb = new StringBuilder($"ID: {LibraryId}, Name: {Name}\nList of books:");
            Books.ForEach(x => sb.AppendLine(x.ToString()));
            return sb.ToString();
        }
    }
}