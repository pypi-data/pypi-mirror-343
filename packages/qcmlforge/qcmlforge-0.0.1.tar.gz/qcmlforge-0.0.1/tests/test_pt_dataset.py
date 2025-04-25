from apnet_pt.AtomPairwiseModels.apnet2 import APNet2Model
from apnet_pt.AtomPairwiseModels.dapnet2 import dAPNet2Model, APNet2_dAPNet2Model
from apnet_pt import AtomPairwiseModels
from apnet_pt import atomic_datasets
from apnet_pt import pairwise_datasets
from apnet_pt import AtomModels
from apnet_pt.pairwise_datasets import (
    apnet2_module_dataset,
    apnet2_collate_update,
    apnet2_collate_update_prebatched,
    APNet2_DataLoader,
    apnet3_module_dataset,
    apnet3_collate_update,
    apnet3_collate_update_prebatched,
)
from apnet_pt.pt_datasets.dapnet_ds import (
    dapnet2_module_dataset,
    dapnet2_module_dataset_apnetStored,
)
import pickle
import os
import numpy as np
import pytest
from glob import glob

spec_type = 5
current_file_path = os.path.dirname(os.path.realpath(__file__))
data_path = f"{current_file_path}/test_data_path"
am_path = f"{current_file_path}/../src/apnet_pt/models/am_ensemble/am_0.pt"
am_hf_path = f"{current_file_path}/../src/apnet_pt/models/am_hf_ensemble/am_0.pt"


def test_apnet2_dataset_size_no_prebatched():
    batch_size = 2
    atomic_batch_size=4
    datapoint_storage_n_objects=8
    prebatched = False
    collate = apnet2_collate_update_prebatched if prebatched else apnet2_collate_update
    ds = apnet2_module_dataset(
        root=data_path,
        r_cut=5.0,
        r_cut_im=8.0,
        spec_type=8,
        max_size=None,
        force_reprocess=True,
        atom_model_path=am_path,
        atomic_batch_size=atomic_batch_size,
        datapoint_storage_n_objects=datapoint_storage_n_objects,
        batch_size=batch_size,
        prebatched=prebatched,
        num_devices=1,
        skip_processed=False,
        skip_compile=True,
        # split="test",
        print_level=2,
    )
    print()
    print(ds)

    train_loader = APNet2_DataLoader(
        dataset=ds,
        # batch_size=1,
        batch_size=ds.training_batch_size,
        shuffle=False,
        num_workers=1,
        # collate_fn=apnet2_collate_update_prebatched,
        collate_fn=collate,
    )
    cnt = 0
    for i in train_loader:
        cnt += i.y.shape[0]
    print("Number of labels in dataset:", cnt)
    ds_labels = len(ds)
    for i in glob(f"{data_path}/processed/dimer_ap2_spec_8*.pt"):
        os.remove(i)
    assert ds_labels == cnt, f"Expected {len(ds)} points, but got {cnt} points"

def test_apnet2_dataset_size_prebatched():
    batch_size = 2
    atomic_batch_size=4
    datapoint_storage_n_objects=8
    prebatched = True
    collate = apnet2_collate_update_prebatched if prebatched else apnet2_collate_update
    ds = apnet2_module_dataset(
        root=data_path,
        r_cut=5.0,
        r_cut_im=8.0,
        spec_type=8,
        max_size=None,
        force_reprocess=True,
        atom_model_path=am_path,
        atomic_batch_size=atomic_batch_size,
        datapoint_storage_n_objects=datapoint_storage_n_objects,
        batch_size=batch_size,
        prebatched=prebatched,
        num_devices=1,
        skip_processed=False,
        skip_compile=True,
        print_level=2,
    )
    print()
    print(ds)
    print(ds.training_batch_size)

    train_loader = APNet2_DataLoader(
        dataset=ds,
        # batch_size=1,
        batch_size=ds.training_batch_size,
        shuffle=False,
        num_workers=1,
        # collate_fn=apnet2_collate_update_prebatched,
        collate_fn=collate,
    )
    cnt = 0
    for i in train_loader:
        cnt += i.y.shape[0]
    print("Number of labels in dataset:", cnt)
    ds_labels = len(ds)
    for i in glob(f"{data_path}/processed/dimer_ap2_spec_8*.pt"):
        os.remove(i)
    assert ds_labels * ds.batch_size == cnt, f"Expected {len(ds) * ds.batch_size} points, but got {cnt} points"


def test_apnet2_dataset_size_prebatched_train_spec8():
    batch_size = 2
    atomic_batch_size=4
    datapoint_storage_n_objects=8
    prebatched = True
    collate = apnet2_collate_update_prebatched if prebatched else apnet2_collate_update
    ds = apnet2_module_dataset(
        root=data_path,
        r_cut=5.0,
        r_cut_im=8.0,
        spec_type=8,
        max_size=None,
        force_reprocess=True,
        atom_model_path=am_path,
        atomic_batch_size=atomic_batch_size,
        datapoint_storage_n_objects=datapoint_storage_n_objects,
        batch_size=batch_size,
        prebatched=prebatched,
        num_devices=1,
        skip_processed=False,
        skip_compile=True,
        # split="test",
        print_level=2,
    )
    print()
    print(ds)
    print(ds.training_batch_size)
    ap2 = APNet2Model().set_pretrained_model(model_id=0)
    ap2.train(
        ds,
        n_epochs=2,
        skip_compile=True,
    )

def test_apnet2_dataset_size_prebatched_train_spec9():
    batch_size = 2
    atomic_batch_size=4
    datapoint_storage_n_objects=8
    prebatched = True
    collate = apnet2_collate_update_prebatched if prebatched else apnet2_collate_update
    ds = apnet2_module_dataset(
        root=data_path,
        r_cut=5.0,
        r_cut_im=8.0,
        spec_type=9,
        max_size=None,
        force_reprocess=True,
        atom_model_path=am_path,
        atomic_batch_size=atomic_batch_size,
        datapoint_storage_n_objects=datapoint_storage_n_objects,
        batch_size=batch_size,
        prebatched=prebatched,
        num_devices=1,
        skip_processed=False,
        skip_compile=True,
        split="train",
        print_level=2,
    )
    print()
    print(ds)
    print(ds.training_batch_size)
    ap2 = APNet2Model().set_pretrained_model(model_id=0)
    ap2.train(
        ds,
        n_epochs=2,
        skip_compile=True,
    )

def test_dapnet2_dataset_size_no_prebatched():
    batch_size = 2
    atomic_batch_size=4
    datapoint_storage_n_objects=8
    prebatched = False
    collate = apnet2_collate_update_prebatched if prebatched else apnet2_collate_update
    ds = dapnet2_module_dataset(
        root=data_path,
        r_cut=5.0,
        r_cut_im=8.0,
        spec_type=8,
        max_size=None,
        force_reprocess=True,
        atom_model_path=am_path,
        atomic_batch_size=atomic_batch_size,
        datapoint_storage_n_objects=datapoint_storage_n_objects,
        batch_size=batch_size,
        prebatched=prebatched,
        num_devices=1,
        skip_processed=False,
        skip_compile=True,
        # split="test",
        print_level=2,
        m1="Elst_aug", 
        m2="Exch_aug",
    )
    print()
    print(ds)

    train_loader = APNet2_DataLoader(
        dataset=ds,
        # batch_size=1,
        batch_size=ds.training_batch_size,
        shuffle=False,
        num_workers=1,
        # collate_fn=dapnet2_collate_update_prebatched,
        collate_fn=collate,
    )
    cnt = 0
    for i in train_loader:
        cnt += i.y.shape[0]
    print("Number of labels in dataset:", cnt)
    ds_labels = len(ds)
    for i in glob(f"{data_path}/processed_delta/dimer_dap2_spec_8_Elstaug_to_Exchaug_*.pt"):
        os.remove(i)
    assert ds_labels == cnt, f"Expected {len(ds)} points, but got {cnt} points"

def test_dapnet2_dataset_size_prebatched():
    batch_size = 2
    atomic_batch_size=4
    datapoint_storage_n_objects=8
    prebatched = True
    collate = apnet2_collate_update_prebatched if prebatched else apnet2_collate_update
    for i in glob(f"{data_path}/processed_delta/dimer_dap2_spec_8_Elst_aug_to_Exch_aug_*.pt"):
        os.remove(i)
    ds = dapnet2_module_dataset(
        root=data_path,
        r_cut=5.0,
        r_cut_im=8.0,
        spec_type=8,
        max_size=None,
        force_reprocess=True,
        atom_model_path=am_path,
        atomic_batch_size=atomic_batch_size,
        datapoint_storage_n_objects=datapoint_storage_n_objects,
        batch_size=batch_size,
        prebatched=prebatched,
        num_devices=1,
        skip_processed=False,
        skip_compile=True,
        print_level=2,
        m1="Elst_aug", 
        m2="Exch_aug",
    )
    print()
    print(ds)
    print(ds.training_batch_size)

    train_loader = APNet2_DataLoader(
        dataset=ds,
        batch_size=ds.training_batch_size,
        shuffle=False,
        num_workers=1,
        collate_fn=collate,
    )
    cnt = 0
    for i in train_loader:
        cnt += i.y.shape[0]
    print("Number of labels in dataset:", cnt)
    ds_labels = len(ds)
    for i in glob(f"{data_path}/processed_delta/dimer_dap2_spec_8_Elst_aug_to_Exch_aug_*.pt"):
        os.remove(i)
    assert ds_labels * ds.batch_size == cnt, f"Expected {len(ds) * ds.batch_size} points, but got {cnt} points"


def test_dapnet2_dataset_ap2_stored_size_prebatched():
    batch_size = 2
    datapoint_storage_n_objects=8
    prebatched = True
    collate = apnet2_collate_update_prebatched if prebatched else apnet2_collate_update
    for i in glob(f"{data_path}/processed_delta/dimer_dap2_ap2_spec_8_*.pt"):
        os.remove(i)
    ds = dapnet2_module_dataset_apnetStored(
        root=data_path,
        r_cut=5.0,
        r_cut_im=8.0,
        spec_type=8,
        max_size=None,
        force_reprocess=True,
        atom_model_path=am_path,
        batch_size=batch_size,
        datapoint_storage_n_objects=datapoint_storage_n_objects,
        prebatched=prebatched,
        num_devices=1,
        skip_processed=False,
        skip_compile=True,
        print_level=2,
        m1="Elst_aug", 
        m2="Exch_aug",
    )
    print()
    print(ds)
    print(ds.training_batch_size)

    train_loader = APNet2_DataLoader(
        dataset=ds,
        batch_size=ds.training_batch_size,
        shuffle=False,
        num_workers=1,
        collate_fn=collate,
    )
    cnt = 0
    for i in train_loader:
        cnt += i.y.shape[0]
        print(i)
        print(i.y)
    print("Number of labels in dataset:", cnt)
    ds_labels = int(len(ds))
    print("Number of labels in dataset:", ds_labels)
    for i in glob(f"{data_path}/processed_delta/dimer_dap2_ap2_spec_8_*.pt"):
        os.remove(i)
    for i in glob(f"{data_path}/processed_delta/targets_Elst_aug_to_Exch_aug.pt"):
        os.remove(i)
    assert ds_labels * ds.batch_size - 1 == cnt, f"Expected {ds_labels * ds.batch_size - 1} points, but got {cnt} points"
    

def test_dapnet2_dataset_ap2_stored_size_prebatched_train():
    batch_size = 2
    atomic_batch_size=4
    datapoint_storage_n_objects=8
    prebatched = True
    print(am_path)
    for i in glob(f"{data_path}/processed_delta/dimer_dap2_spec_8_Elst_aug_to_Exch_aug_*.pt"):
        os.remove(i)
    ds = dapnet2_module_dataset_apnetStored(
        root=data_path,
        r_cut=5.0,
        r_cut_im=8.0,
        spec_type=8,
        max_size=None,
        force_reprocess=True,
        atom_model_path=am_path,
        batch_size=batch_size,
        datapoint_storage_n_objects=datapoint_storage_n_objects,
        prebatched=prebatched,
        num_devices=1,
        skip_processed=False,
        skip_compile=True,
        print_level=2,
        m1="Elst_aug", 
        m2="Exch_aug",
    )
    apnet2_model = APNet2Model().set_pretrained_model(model_id=0)
    apnet2_model.model.return_hidden_states = True
    dapnet2 = dAPNet2Model(
        apnet2_model=apnet2_model,
        dataset=ds
    )
    dapnet2.train(
        n_epochs=2,
        skip_compile=True,
    )
    for i in glob(f"{data_path}/processed_delta/dimer_dap2_spec_8_Elst_aug_to_Exch_aug_*.pt"):
        os.remove(i)
    return

def test_dapnet2_dataset_size_prebatched_train():
    batch_size = 2
    atomic_batch_size=4
    datapoint_storage_n_objects=8
    prebatched = True
    print(am_path)
    for i in glob(f"{data_path}/processed_delta/dimer_dap2_spec_8_Elst_aug_to_Exch_aug_*.pt"):
        os.remove(i)
    ds = dapnet2_module_dataset(
        root=data_path,
        r_cut=5.0,
        r_cut_im=8.0,
        spec_type=8,
        max_size=None,
        force_reprocess=True,
        atom_model_path=am_path,
        atomic_batch_size=atomic_batch_size,
        datapoint_storage_n_objects=datapoint_storage_n_objects,
        batch_size=batch_size,
        prebatched=prebatched,
        num_devices=1,
        skip_processed=False,
        skip_compile=True,
        print_level=2,
        m1="Elst_aug", 
        m2="Exch_aug",
    )
    apnet2_model = APNet2Model().set_pretrained_model(model_id=0).model
    apnet2_model.return_hidden_states = True
    dapnet2 = APNet2_dAPNet2Model(
        apnet2_mpnn=apnet2_model,
        dataset=ds
    )
    dapnet2.train(
        n_epochs=2,
        skip_compile=True,
    )
    for i in glob(f"{data_path}/processed_delta/dimer_dap2_spec_8_Elst_aug_to_Exch_aug_*.pt"):
        os.remove(i)
    return


def test_apnet3_dataset_size_no_prebatched():
    batch_size = 2
    atomic_batch_size=4
    datapoint_storage_n_objects=8
    prebatched = False
    collate = apnet3_collate_update_prebatched if prebatched else apnet3_collate_update
    ds = apnet3_module_dataset(
        root=data_path,
        r_cut=5.0,
        r_cut_im=8.0,
        spec_type=8,
        max_size=None,
        force_reprocess=True,
        atom_model_path=am_hf_path,
        atomic_batch_size=atomic_batch_size,
        datapoint_storage_n_objects=datapoint_storage_n_objects,
        batch_size=batch_size,
        prebatched=prebatched,
        num_devices=1,
        skip_processed=False,
        skip_compile=True,
        # split="test",
        print_level=2,
    )
    print()
    print(ds)
    

    train_loader = APNet2_DataLoader(
        dataset=ds,
        # batch_size=1,
        batch_size=ds.training_batch_size,
        shuffle=False,
        num_workers=1,
        # collate_fn=apnet2_collate_update_prebatched,
        collate_fn=collate,
    )
    cnt = 0
    for i in train_loader:
        cnt += i.y.shape[0]
    print("Number of labels in dataset:", cnt)
    ds_labels = len(ds)
    for i in glob(f"{data_path}/processed/dimer_ap3_spec_8*.pt"):
        os.remove(i)
    assert ds_labels == cnt, f"Expected {len(ds)} points, but got {cnt} points"

def test_apnet3_dataset_size_prebatched():
    batch_size = 2
    atomic_batch_size=4
    datapoint_storage_n_objects=8
    prebatched = True
    collate = apnet3_collate_update_prebatched if prebatched else apnet3_collate_update
    ds = apnet3_module_dataset(
        root=data_path,
        r_cut=5.0,
        r_cut_im=8.0,
        spec_type=8,
        max_size=None,
        force_reprocess=True,
        atom_model_path=am_hf_path,
        atomic_batch_size=atomic_batch_size,
        datapoint_storage_n_objects=datapoint_storage_n_objects,
        batch_size=batch_size,
        prebatched=prebatched,
        num_devices=1,
        skip_processed=False,
        skip_compile=True,
        # split="test",
        print_level=2,
    )
    print()
    print(ds)
    print(ds.training_batch_size)

    train_loader = APNet2_DataLoader(
        dataset=ds,
        # batch_size=1,
        batch_size=ds.training_batch_size,
        shuffle=False,
        num_workers=1,
        # collate_fn=apnet3_collate_update_prebatched,
        collate_fn=collate,
    )
    cnt = 0
    for i in train_loader:
        cnt += i.y.shape[0]
    print("Number of labels in dataset:", cnt)
    ds_labels = len(ds)
    for i in glob(f"{data_path}/processed/dimer_ap3_spec_8*.pt"):
        os.remove(i)
    assert ds_labels * ds.batch_size == cnt, f"Expected {len(ds) * ds.batch_size} points, but got {cnt} points"


def test_apnet2_model_train():
    ds = apnet2_module_dataset(
        root=data_path,
        r_cut=5.0,
        r_cut_im=8.0,
        spec_type=5,
        max_size=None,
        force_reprocess=False,
        atom_model_path=am_path,
        atomic_batch_size=1000,
        num_devices=1,
        skip_processed=False,
        split="train",
    )
    apnet2 = APNet2Model(
        dataset=ds,
        ds_root=data_path,
        ds_spec_type=spec_type,
        ds_force_reprocess=False,
        ignore_database_null=False,
        ds_atomic_batch_size=1000,
        ds_num_devices=1,
        ds_skip_process=False,
        # ds_max_size=10,
    ).set_pretrained_model(model_id=0)
    apnet2.train(
        model_path="./models/ap2_test.pt",
        n_epochs=1,
        world_size=1,
        omp_num_threads_per_process=8,
        lr=2e-3,
        lr_decay=0.10,
        # lr_decay=None,
        skip_compile=True,
    )
    return

def test_apnet2_model_train_small():
    ds = apnet2_module_dataset(
        root=data_path,
        r_cut=5.0,
        r_cut_im=8.0,
        spec_type=5,
        max_size=None,
        force_reprocess=False,
        atom_model_path=am_path,
        batch_size=2,
        atomic_batch_size=4,
        num_devices=1,
        skip_processed=False,
        skip_compile=True,
        split="train",
    )
    apnet2 = APNet2Model(
        dataset=ds,
        ds_root=data_path,
        ds_spec_type=spec_type,
        ds_force_reprocess=False,
        ignore_database_null=False,
        ds_atomic_batch_size=4,
        ds_num_devices=1,
        ds_skip_process=False,
        # ds_max_size=10,
    ).set_pretrained_model(model_id=0)
    apnet2.train(
        model_path="./models/ap2_test.pt",
        n_epochs=1,
        world_size=1,
        omp_num_threads_per_process=8,
        lr=2e-3,
        lr_decay=0.10,
        skip_compile=True,
        # lr_decay=None,
    )
    return


def test_apnet2_model_train_small_r_cut_im():
    r_cut_im = 16.0
    n_rbf=12
    ds = apnet2_module_dataset(
        root=data_path,
        r_cut=5.0,
        r_cut_im=r_cut_im,
        spec_type=5,
        max_size=None,
        force_reprocess=True,
        atom_model_path=am_path,
        batch_size=2,
        atomic_batch_size=4,
        num_devices=1,
        skip_processed=False,
        skip_compile=True,
        split="train",
    )
    apnet2 = APNet2Model(
        dataset=ds,
        ds_root=data_path,
        ds_spec_type=spec_type,
        r_cut_im=r_cut_im,
        n_rbf=n_rbf,
        ds_force_reprocess=False,
        ignore_database_null=False,
        ds_atomic_batch_size=4,
        ds_num_devices=1,
        ds_skip_process=False,
        # ds_max_size=10,
    )
    apnet2.train(
        model_path="./models/ap2_test_r_cut_im.pt",
        n_epochs=1,
        world_size=1,
        omp_num_threads_per_process=8,
        lr=2e-3,
        lr_decay=0.10,
        skip_compile=True,
        # lr_decay=None,
    )
    return

def test_atomhirshfeld_model_train():
    ds = atomic_datasets.atomic_hirshfeld_module_dataset(
        root=data_path,
        transform=None,
        pre_transform=None,
        r_cut=5.0,
        testing=False,
        spec_type=5,
        max_size=None,
        force_reprocess=False,
        in_memory=True,
        batch_size=1,
    )
    print(ds)
    am = AtomModels.ap3_atom_model.AtomHirshfeldModel(
        use_GPU=False,
        ignore_database_null=False,
        dataset=ds,
    )
    print(am)
    am.train(
        n_epochs=5,
        batch_size=1,
        lr=5e-4,
        split_percent=0.5,
        model_path=None,
        optimize_for_speed=False,
        shuffle=True,
        dataloader_num_workers=0,
        world_size=1,
        omp_num_threads_per_process=None,
        random_seed=42,
    )
    return


def test_atomhirshfeld_model_train():
    ds = atomic_datasets.atomic_hirshfeld_module_dataset(
        root=data_path,
        transform=None,
        pre_transform=None,
        r_cut=5.0,
        testing=False,
        spec_type=5,
        max_size=None,
        force_reprocess=False,
        in_memory=True,
        batch_size=1,
    )
    print(ds)
    am = AtomModels.ap3_atom_model.AtomHirshfeldModel(
        use_GPU=False,
        ignore_database_null=False,
        dataset=ds,
    )
    print(am)
    am.train(
        n_epochs=5,
        batch_size=1,
        lr=5e-4,
        split_percent=0.5,
        model_path=None,
        optimize_for_speed=False,
        shuffle=True,
        dataloader_num_workers=0,
        world_size=1,
        omp_num_threads_per_process=None,
        random_seed=42,
    )
    return


@pytest.mark.skip(reason="Skip this test for large ap3 dataset")
def test_ap3_model_train():
    world_size = 1
    print("World Size", world_size)

    batch_size = 16
    omp_num_threads_per_process = 8
    apnet3 = AtomPairwiseModels.apnet3.APNet3Model(
        atom_model_pre_trained_path="./models/am_hf_ensemble/am_4.pt",
        pre_trained_model_path=None,
        ds_spec_type=7,
        ds_root=data_path,
        ignore_database_null=False,
        ds_atomic_batch_size=200,
        ds_num_devices=1,
        ds_skip_process=False,
        ds_datapoint_storage_n_objects=batch_size,
        ds_prebatched=True,
    )
    apnet3.train(
        model_path="./ap3_test.pt",
        n_epochs=5,
        world_size=world_size,
        omp_num_threads_per_process=omp_num_threads_per_process,
        lr=5e-4,
        dataloader_num_workers=4,
        random_seed=4,
        skip_compile=True,
    )


if __name__ == "__main__":
    # test_apnet_data_object()
    # test_apnet3_dataset_size_no_prebatched()
    # test_apnet3_dataset_size_prebatched()
    # test_apnet2_model_train()
    # test_atomhirshfeld_model_train()
    # test_ap3_model_train()
    # test_dapnet2_dataset_size_prebatched_rcut()
    # test_apnet2_model_train_small_r_cut_im()
    test_dapnet2_dataset_ap2_stored_size_prebatched()
    pass
