package Storage;

import java.util.*;

public class Disk {
	private static final String TAG = "Disk";
	int diskSize;
	int maxBlockCount;
	int blockSize;
	int recordCounts;
	ArrayList<Block> blocks;

	public Disk(int diskSize, int blockSize) {
		this.diskSize = diskSize;
		this.blockSize = blockSize;
		this.maxBlockCount = diskSize / blockSize;
		this.blocks = new ArrayList<>();
		this.recordCounts = 0;
	}

	/**
	 * Get the total number of blocks exist in the storage
	 * 
	 * @return
	 */
	public int getBlocksCount() {
		return blocks.size();
	}

	/**
	 * Get the total number of records exist in the storage
	 * 
	 * @return
	 */
	public int getRecordCounts() {
		return recordCounts;
	}

	/**
	 * Get the used size of storage
	 * 
	 * @return
	 */
	public int getUsedSize() {
		return getBlocksCount() * blockSize;
	}

	/**
	 * insert the records into first available block for record insertion, however,
	 * it can be expensive!!!
	 * 
	 * @param record inserting record
	 * @return address of record being inserted
	 * @throws Exception
	 */
	public Address insertRecord(Record record) throws Exception {
		int blockId = getFirstAvailableBlockId();
		return insertRecordAt(blockId, record);
	}

	/**
	 * Attempt to insert record into last block. if last block is not available,
	 * record will be inserted into newly created block. noted that on no checking
	 * of availability will be done on prev blocks
	 * 
	 * @param record inserting record
	 * @return address of record being inserted
	 * @throws Exception
	 */
	public Address appendRecord(Record record) throws Exception {
		int blockId = getLastBlockId();
		return insertRecordAt(blockId, record);
	}

	private Address insertRecordAt(int blockId, Record record) throws Exception {
		Block block = null;
		if (blockId >= 0) {
			block = getBlockAt(blockId);
		}

		// block is not available/not exist, try to create a new block to insert the
		// record
		if (block == null || !block.isAvailable()) {
			if (blocks.size() == maxBlockCount) {
				throw new Exception("Insufficient spaces on disk");
			}
			block = new Block(blockSize);
			blocks.add(block);
			blockId = getLastBlockId();
		}
		int offset = block.insertRecord(record);
		recordCounts++;
		return new Address(blockId, offset);
	}

	public int getFirstAvailableBlockId() {
		int blockId = -1;
		for (int i = 0; i < blocks.size(); i++) {
			if (blocks.get(i).isAvailable()) {
				blockId = i;
				break;
			}
		}
		return blockId;
	}

	public int getLastBlockId() {
		return blocks.size() > 0 ? blocks.size() - 1 : -1;
	}

	public Block getBlockAt(int blockId) {
		return blocks.get(blockId);
	}

	public Record getRecordAt(int blockId, int offset) {
		return getBlockAt(blockId).getRecordAt(offset);
	}

	public Record getRecordAt(Address address) {
		return getRecordAt(address.getBlockId(), address.getOffset());
	}

	public ArrayList<Record> getRecords(ArrayList<Address> addresses) {
		// addresses.sort(Comparator.comparingInt(Address::getBlockId));
		HashMap<Integer, Block> cache = new HashMap<>();
		ArrayList<Record> records = new ArrayList<>();
		int blockAccess = 0;
		Block tempBlock = null;
		for (Address address : addresses) {
			// try search from cache first, before access from disk
			tempBlock = cache.get(address.getBlockId());
			//boolean cacheRead = tempBlock != null;
			if (tempBlock == null) {
				tempBlock = getBlockAt(address.getBlockId());
				cache.put(address.getBlockId(), tempBlock);
				blockAccess++;
			}// accessing the block from cache, no block access
			Record record = tempBlock.getRecordAt(address.getOffset());
			records.add(record);
		}
		System.out.println("data block access is: "+blockAccess+" with "+records.size()+" records found");
		return records;
	}

	// GET ALL RECORDS WITH KEY == 500 by scanning the disk linearly
	public ArrayList<Record> getRecordsByBruteForce(int key) {
		ArrayList<Record> records = new ArrayList<>();
		int blockAccess = 0;

		for (int i = 0; i < this.blocks.size(); i++) {
			blockAccess++;
			for(int j = 0; j< getBlockAt(i).curRecords; j++) {
				if(key == getBlockAt(i).getRecordAt(j).getNumVotes()) {
					records.add(getBlockAt(i).getRecordAt(j));
				}
			}
		}
		//System.out.println("Size of result: "+records.size());
		System.out.println("Brute-force data block access is: "+blockAccess + " with "+records.size()+" records found");

		return records;
	}
	
	//experiement 4 bruteforce
	public ArrayList<Record> getRecordsByBruteForce(int start, int end) {
		ArrayList<Record> records = new ArrayList<>();
		int blockAccess = 0;

		for (int i = 0; i < this.blocks.size(); i++) {
			blockAccess++;
			for(int j = 0; j< getBlockAt(i).curRecords; j++) {
				if((getBlockAt(i).getRecordAt(j).getNumVotes() >= start) && (getBlockAt(i).getRecordAt(j).getNumVotes() <= end)) {
					records.add(getBlockAt(i).getRecordAt(j));
				}
			}
		}
		//System.out.println("Size of result: "+records.size());
		System.out.println("Brute-force data block access is: "+blockAccess + " with "+records.size()+" records found");

		return records;
	}
	
	//experiment 5 bruteforce delete
		public ArrayList<Record> deleteRecordsByBruteForce(int key) {
			ArrayList<Address> recordsToDelete = new ArrayList<>();
			ArrayList<Record> recordsDeleted = new ArrayList<>();
			int blockAccess = 0;
			//int foundRecordToDelete = 0;

			for (int i = 0; i < this.blocks.size(); i++) {
				blockAccess++;
				for(int j = 0; j< getBlockAt(i).curRecords; j++) {
					if(getBlockAt(i).getRecordAt(j).getNumVotes() == key) {
						//foundRecordToDelete++;
						Address addressToDelete = new Address(i,j);
						recordsToDelete.add(addressToDelete);
						recordsDeleted.add(getBlockAt(i).getRecordAt(j));
					}
				}
				deleteRecords(recordsToDelete);
				recordsToDelete.clear();
			}
			//System.out.println("Size of result: "+recordsDeleted.size());
			System.out.println("Brute-force data block access is: "+blockAccess + " with "+recordsDeleted.size()+" deleted records found");
			return recordsDeleted;
		}

	public boolean deleteRecordAt(int blockId, int offset) {
		boolean success = getBlockAt(blockId).deleteRecordAt(offset);
		if (success) {
			recordCounts--;
		}
		return success;
	}

	public void deleteRecords(ArrayList<Address> recordAddresses) {
		for (Address address : recordAddresses) {
			deleteRecordAt(address.getBlockId(), address.getOffset());
		}
	}

}