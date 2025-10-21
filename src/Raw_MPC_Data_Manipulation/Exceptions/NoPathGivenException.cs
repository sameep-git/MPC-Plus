using System;

namespace MPC_Plus.Exceptions
{
    // Custom exception for when a bad or missing path is given
    public class NoPathGivenException : Exception
    {
        // Default constructor
        public NoPathGivenException()
        {
        }

        // Constructor with custom message
        public NoPathGivenException(string message)
            : base(message)
        {
        }

        // Constructor with custom message and inner exception (for chaining)
        public NoPathGivenException(string message, Exception inner)
            : base(message, inner)
        {
        }
    }
}
