package Storage;

public class Record {
    public String tconst;
    public float avgRating;
    public int numVotes;

    public Record(String tconst, float avgRating, int numVotes) {
        this.tconst = tconst;
        this.avgRating = avgRating;
        this.numVotes = numVotes;
    }

    public String getTconst() {
        return tconst;
    }

    public void setTconst(String tconst) {
        this.tconst = tconst;
    }

    public float getAvgRating() {
        return avgRating;
    }

    public void setAvgRating(float avgRating) {
        this.avgRating = avgRating;
    }

    public int getNumVotes() {
        return numVotes;
    }

    public void setNumVotes(int numVotes) {
        this.numVotes = numVotes;
    }

    public static int size(){
        return 18;
    }

    @Override
    public String toString() {
        return "{" + tconst + "; " + avgRating + "; " + numVotes + "}";
    }
}
