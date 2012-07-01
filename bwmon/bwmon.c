#include <stdio.h>
#include <unistd.h>
#include <sys/time.h>

void skipline(FILE *f)
{
  int ch;
  do {
    ch = getc(f);
  } while ( ch != '\n' && ch != EOF );
}


int main(int argc, char* argv[]) {
    struct timeval t_now, t_last;
    FILE *fp;

    char *interface = "eth0";
    char *outfile = "usage";
    unsigned long interval = 100000; // usecs
    int NUM_AVERAGE = 10;

    unsigned int lastin = 0;
    unsigned int lastout = 0;
    unsigned int diffin, diffout;
    double maxin=0, maxout=0;
    double bwin, bwout;
    double timedelta;
    double inav[NUM_AVERAGE];
    double outav[NUM_AVERAGE];
    int curr=0, tmp;
    double outa, ina;
    int i;
    struct ifinfo {
        char name[8];
        unsigned int r_bytes, r_pkt, r_err, r_drop, r_fifo, r_frame;
        unsigned int r_compr, r_mcast;
        unsigned int x_bytes, x_pkt, x_err, x_drop, x_fifo, x_coll;
        unsigned int x_carrier, x_compr;
    } ifc;

    for(i=0;i<NUM_AVERAGE;i++) {
	inav[i]=0; outav[i]=0;
    }

    for(;;) {
        gettimeofday(&t_now, NULL);
        fp = fopen("/proc/net/dev", "r");
        skipline(fp);
        skipline(fp);
        do {
            if ( fscanf(fp, " %6[^:]:%u %u %u %u %u %u %u %u %u %u %u %u %u %u %u %u",
                        ifc.name,
                        &ifc.r_bytes, &ifc.r_pkt, &ifc.r_err, &ifc.r_drop,
                        &ifc.r_fifo, &ifc.r_frame, &ifc.r_compr, &ifc.r_mcast,
                        &ifc.x_bytes, &ifc.x_pkt, &ifc.x_err, &ifc.x_drop,
                        &ifc.x_fifo, &ifc.x_coll, &ifc.x_carrier, &ifc.x_compr)
                 != 17 ) {
              exit(200);
          }
          skipline(fp);
        } while ( strcmp(ifc.name, interface) );
        fclose(fp);

        if(lastin == 0) lastin = ifc.r_bytes;
        if(lastout == 0) lastout = ifc.x_bytes;

        diffin = ifc.r_bytes - lastin;
	diffout = ifc.x_bytes - lastout;

        timedelta = (double)(t_now.tv_sec - t_last.tv_sec) + (t_now.tv_usec - t_last.tv_usec)/1.0e+6;

        bwin = diffin / timedelta * 8;
	bwout = diffout / timedelta * 8;

	inav[curr] = bwin;
	outav[curr] = bwout;
	curr += 1; curr %= NUM_AVERAGE;

	ina=0; outa=0;
	for(i=0;i<NUM_AVERAGE;i++) {
	    ina+=inav[i]; outa+=outav[i];
	}
	ina /= NUM_AVERAGE; outa /= NUM_AVERAGE;

        if(maxin<ina) maxin = ina;
        if(maxout<outa) maxout = outa;

        t_last = t_now; lastin = ifc.r_bytes; lastout = ifc.x_bytes;

        fp=fopen(outfile, "w");
	fprintf(fp, "%f %f %f %f %f %f\n", ina, outa, maxin, maxout, bwin, bwout);
	fclose(fp);

	usleep(interval);
    }
}

