using Projekt_web.Models.DbModels;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace Projekt_web.Models
{
    public class RentedBook
    {
        public RentedBook()
        {
        }

        public RentedBook(int rentedBookId, int bookId, int userId, DateTime rentDate)
        {
            RentedBookId = rentedBookId;
            BookId = bookId;
            UserId = userId;
            RentDate = rentDate;
        }
        public virtual Book Book { get; set; }
        public virtual User User { get; set; }
        public int RentedBookId { get; set; }
        public int BookId { get; set; }
        public int UserId { get; set; }
        [DataType(DataType.Date)]
        [DisplayFormat(DataFormatString = "{0:yyyy-MM-dd}", ApplyFormatInEditMode = true)]
        public DateTime RentDate { get; set; }
        [DataType(DataType.Date)]
        [DisplayFormat(DataFormatString = "{0:yyyy-MM-dd}", ApplyFormatInEditMode = true)]
        public DateTime ReturnDate { get; set; }
        public int Penalty { get; set; }
    }
}