 
#define DICTFILE "mrc2.dct"
#define MAXREC 200	/* maximum record size in either file */
#define MAXWORD 30	/* maximum word length */
#define WORDSTART 51	/* first char of word entry in dictionary */

#include <stdio.h>
#include <stdlib.h>

static FILE  *fpdin, *fpnin, *fperr;
static char outline[MAXREC], dictline[MAXREC], dictword[MAXWORD];
static char newline[MAXREC],newword[MAXWORD], *infile;
static int  dictwordlen, newwordlen, maxlen;

static readnew()
{
int i,j;
/* read new line to give: line, word and word length*/
	i = 0;
	if (fgets(newline, MAXREC, fpnin) != NULL) {
		while (newline[i] != '\n'){
			if (newline[i] >= 'a' && newline[i] <= 'z')
				newword[i] = (newline[i] - 32);
			else newword[i] = newline[i];
			i++;
		}
	if (newword[i-1] == ' ' || newword[i-1] == '\t') {
		newword[i-1] = '\0';
		newwordlen = (i-1);
	}
	else {
		newword[i] = '\0';
		newwordlen = (i);
	}
		newline[i] = '\0';	
		return(1);
	}
  	else return(0);
}

static openfiles()
{
FILE *fopen();
	    
/* open dictionary file */

       	if ((fpdin = fopen ( DICTFILE, "r")) == NULL) {
	   fprintf(stderr, " can't open %s  as data file \n", DICTFILE);
	   exit(0);
	   }

/* open new entry file */

       	if ((fpnin = fopen ( infile, "r")) == NULL) {
	   fprintf(stderr, " can't open %s  as new file \n", infile);
	   exit(0);
	   }
}

static readdict()
{
int i,j;

/* read dictionary line to give: line, word and word length*/

	if (fgets(dictline, MAXREC, fpdin) != NULL) {
		i = WORDSTART;
		j = 0;
		while (dictline[i] != '|'){
			dictword[j] = dictline[i]; /* word itself*/
			i++;
			j++;
		}
		dictword[j] = '\0';
		dictwordlen = j;
		i=0;
		while(dictline[i] != '\n'){i++;}
		dictline[i] = '\0';	
		return(1);
	}
  	else return(0);
}

main(argc,argv)
int argc;
char *argv[];
{
int i,j,k,n, lastmatchchar, equal;

	if (argc < 2) {
		fprintf(stderr, "Usage: getentry filename\n\n");
		fprintf(stderr, "giving the name of a file containing a sorted list of words\n");
		exit(0);
	}
	else infile = (*++argv);
	
	openfiles();

	if (readdict() == 0)
		exit(0);
	if (readnew() == 0)
		exit(0);

	while (dictwordlen > 0 && newwordlen > 0){

		equal = 0;
		if (dictwordlen < newwordlen){
			maxlen = dictwordlen;
		}
		else if (dictwordlen > newwordlen){
			maxlen = newwordlen;
		}
		else if (dictwordlen == newwordlen){
			maxlen = newwordlen;
			equal = 1;
		}

		i=0;
		while (dictword[i] == newword[i] && i < (maxlen)) i++;
		lastmatchchar = (i-1);

		if (dictword[lastmatchchar+1] < newword[lastmatchchar+1] ){ 
			/* get next dictionary line */
			if (readdict() == 0)
				exit(0);
			
		}
		else if (newword[lastmatchchar+1 ] < dictword[lastmatchchar+1 ]){
			/* go to next new line */
			if (readnew() == 0)
				exit(0);
			
		}
		else if (equal == 1 && lastmatchchar == (maxlen-1)){
			printf("%s\n", dictline);
			if (readdict() == 0) 
				exit(0);
		}
		else  {
			fprintf(stderr, "error: undetected word type %s", newword);
			exit(0);
		}
	}
}
