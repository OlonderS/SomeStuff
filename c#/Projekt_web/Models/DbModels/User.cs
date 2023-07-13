using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Projekt_web.Models.DbModels
{
    public class User
    {
        public int UserId { get; set; }
        public string Name { get; set; }
        public string Surname { get; set; }
        public List<RentedBook> RentedBooks { get; set; }
    }
}