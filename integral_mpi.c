/* C Example */
#include <mpi.h>
#include <math.h>
#include <stdio.h>
#include <time.h>

double fct(double x)
{
      return cos(x);
}

/* Prototype */
double integral(double a, int n, double h);

int main(int argc, char *argv[])


{
      /***********************************************************************
       *                                                                     *
       * This is one of the MPI versions on the integration example          *
       * It demonstrates the use of :                                        *
       *                                                                     *
       * 1) MPI_Init                                                         *
       * 2) MPI_Comm_rank                                                    *
       * 3) MPI_Comm_size                                                    *
       * 4) MPI_Recv                                                         *
       * 5) MPI_Send                                                         *
       * 6) MPI_Finalize                                                     *
       * 7) MPI_allreduce													   *
       *                                                                     *
       ***********************************************************************/
      long int n, i, j, ierr, num;
      double h, result, a, b, pi, global_sum;
      double my_a, my_range;
      time_t start, end;

      if (argc < 2)
      {
            printf("Usage: mpirun -np <num_processes> %s <method: r or sr>\n", argv[0]);
            return 0;
      }

      int myid, source, dest, tag, p;
      double duration;
      MPI_Status status;
      double my_result;

      pi = acos(-1.0);  /* = 3.14159... */
      a = 0.;           /* lower limit of integration */
      b = pi * 1. / 2.; /* upper limit of integration */
      n = 100000000;    /* number of increment within each process */

      dest = 0;  /* define the process that computes the final result */
      tag = 123; /* set the tag to identify this particular job */

      /* Starts MPI processes ... */
      // printf("Print arguments passed to the program:\n");
      // for (int x = 0; x < argc; x++)
      // {
      //       printf("argv[%d] = %s\n", x, argv[x]);
      // }

      MPI_Init(&argc, &argv);               /* starts MPI */
      MPI_Comm_rank(MPI_COMM_WORLD, &myid); /* get current process id */
      MPI_Comm_size(MPI_COMM_WORLD, &p);    /* get number of processes */

      h = (b - a) / n; /* length of increment */
      num = n / p;     /* number of intervals calculated by each process*/
      my_range = (b - a) / p;
      my_a = a + myid * my_range;

      start = clock();
      my_result = integral(my_a, num, h);
      // printf("Process %d has the partial result of %f\n", myid, my_result);

      if (argc >= 2 && argv[1][0] == 'r')
      {
            // Using MPI_Reduce to sum up all partial results
            MPI_Reduce(&my_result, &result, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
            if (myid == 0)
            {
                  // printf("The total integral result using MPI_Reduce = %f\n", result);
            }
      }
      else
      {
            // Using point-to-point communication to sum up all partial results
            if (myid == 0)
            {
                  result = my_result;
                  // printf("integral = %f\n", my_result);
                  for (i = 1; i < p; i++)
                  {
                        source = i; /* MPI process number range is [0,p-1] */
                        MPI_Recv(&my_result, 1, MPI_DOUBLE, source, tag,
                                 MPI_COMM_WORLD, &status);
                        result += my_result;
                        // printf("integral = %f\n", my_result);
                  }
                  // printf("The result with send - receive =%f\n", result);
            }
            else
            {
                  MPI_Send(&my_result, 1, MPI_DOUBLE, dest, tag,
                           MPI_COMM_WORLD); /* send my_result to intended dest.
                                             */
            }
      }
      if (myid == 0)
      {
            end = clock();
            duration = (end - start)/(CLOCKS_PER_SEC*1.0);
            // printf("The total integral result = %f\n", result);
            // printf("Total time taken = %f seconds\n", duration);
            // printf("Method used: %s\n", (argc >= 2 && argv[1][0] == 'r') ? "MPI_Reduce" : "Send-Receive");
            
            
            //open to print as row data
            printf("%s,%d,%f,%f\n", (argc >= 2 && argv[1][0] == 'r') ? "MPI_Reduce" : "Send-Receive", p, result, duration);
      }
      MPI_Finalize(); /* let MPI finish up ... */

      return 0;
}

double integral(double a, int n, double h)
{
      int j;
      double h2, aij, integ;

      integ = 0.0; /* initialize integral */
      h2 = h / 2.;
      for (j = 0; j < n; j++)
      {                      /* sum over all "j" integrals */
            aij = a + j * h; /* lower limit of "j" integral */
            integ += fct(aij + h2) * h;
      }
      return (integ);
}
