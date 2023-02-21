package app;

import java.time.LocalTime;
import java.util.*;

import app.storage.Address;
import app.storage.Disk;
import app.storage.Record;
import Index.BPlusTree;
import app.util.Log;
import app.util.Utility;

public class MainApp implements Constants {
	private static final String TAG = "App";
	Scanner scanner = new Scanner(System.in);
	private Disk disk;
	private BPlusTree index;


	public void run(int blockSize) throws Exception {
		// read records from data file
		List<Record> records = Utility.readRecord(DATA_FILE_PATH);

		disk = new Disk(Constants.DISK_SIZE, blockSize);
		index = new BPlusTree(blockSize);

		Log.i(TAG,"Running program with block size of "+blockSize);
		Log.i(TAG,"Prepare to insert records into storage and create index");
		Address recordAddr;
		for (Record r: records) {
			// inserting records into disk and create index!
			recordAddr = disk.appendRecord(r);
			index.insert( r.getNumVotes(), recordAddr);
		}
		Log.i(TAG,"Record inserted into storage and index created");
		disk.log();
//		index.logStructure(1); // printing root and first level?

		index.treeStats();

		// TODO do experiences
		pause("Press any key to start experiment 3");
		experiment3();
		pause("Press any key to start experiment 4");
		experiment4();
		pause("Press any key to start experiment 5");
		experiment5();
	}

	public void experiment3(){
		System.out.println("Starting Experiment 3......");
		
		//normal B+ scanning 
		LocalTime timeStart = LocalTime.now(); //record start time
		ArrayList<Address> e3RecordAddresses = index.getRecordsWithKey(500);
		LocalTime timeEnd = LocalTime.now(); //record end time
		System.out.println("Start: "+timeStart+" End: "+timeEnd+" time lapse: " + timeEnd.compareTo(timeStart));
		//retrieve all the actual records inside the block
		ArrayList<Record> records = disk.getRecords(e3RecordAddresses);
		System.out.println("Number of records found: "+ records.size());
		
		//bruteforce way
		timeStart = LocalTime.now(); //record start time
		ArrayList<Address> e3RecordAddressesBruteForce = index.getLeafNodeByBruteForce(500,true);
		timeEnd = LocalTime.now(); //record end time
		System.out.println("Start: "+timeStart+" End: "+timeEnd+" time lapse: " + timeEnd.compareTo(timeStart));

		
		double avgRating = 0;
		for (Record record: records) {
			avgRating += record.getAvgRating();
		}
		avgRating /= records.size();
		Log.i("Average rating="+avgRating);
	}

	public void experiment4(){
		Log.i(TAG,"Experience 4 started, getting records with numVotes between 30k-40k ");
		ArrayList<Address> e4RecordAddresses = index.getRecordsWithKeyInRange(30000,40000);
		ArrayList<Record> records = disk.getRecords(e4RecordAddresses);
		// records collected, do calculate average rating
		double avgRating = 0;
		for (Record record: records) {
			avgRating += record.getAvgRating();
		}
		avgRating /= records.size();
		Log.i("Average rating="+avgRating);
	}

	public void experiment5(){
		index.deleteKey(1000);
		// TODO: get back address and delete records from storage
	}

	private void pause(String message){
		if (message == null){
			message = "Press any key to continue";
		}
		System.out.print(message);
		scanner.nextLine();
	}



	public static void main(String[] args) {
		try {
			Log.setLevel(Log.LEVEL_DEBUG);
			MainApp app = new MainApp();
			app.run(BLOCK_SIZE_200);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
