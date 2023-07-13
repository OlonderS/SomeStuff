using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace Projekt_web.Models.DbModels
{
    public class Publisher
    {
        public int PublisherId { get; set; }
        [Required]
        [MaxLength(20)]
        public string Name { get; set; }
        public List<Book> Books { get; set; }
    }
}