using Projekt_web.Models.DbModels;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace Projekt_web.Models
{
    public class Book
    {
        public int BookId { get; set; }
        [Required]
        [MaxLength(20)]
        public string Title { get; set; }
        public string Author { get; set; }
        public string Description { get; set; }
        public virtual Publisher Publisher { get; set; }
        public int PublisherId { get; set; }
        public BookType Category { get; set; }
        public DateTime Date { get; set; }
        public bool Available { get; set; }
    }
    public enum BookType { Fantasy, Other }
}
